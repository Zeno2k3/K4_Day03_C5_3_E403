"""
🚀 CORE AGENT APP (Dành cho Role 4: Core Agent Developer)
File chính ghép nối tất cả các thành phần: Tools + Prompts + Test Cases + Multi-Provider.
"""

import ast
import json
import os
import re
import sys
import time
from dotenv import load_dotenv

# Đảm bảo import các module cùng thư mục src/ hoạt động mượt mà
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Đảm bảo in ra Tiếng Việt và Emojis không bị lỗi trên Windows Console
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Import các thành phần từ file của Role 2, Role 3 & Multi-Provider Adapter
from tools import AVAILABLE_TOOLS
from prompts import CHATBOT_BASELINE_PROMPT, REACT_SYSTEM_PROMPT, MAX_ITERATIONS
from providers import get_llm_provider

load_dotenv()

def load_test_cases():
    """Đọc bộ test cases từ config/test_cases.json của Role 1"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(base_dir, "config", "test_cases.json")
    
    # Fallback kiểm tra nếu file ở thư mục hiện tại
    if not os.path.exists(config_path):
        config_path = "test_cases.json"
        
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def run_rule_based_bot(user_query: str):
    """
    Dựng Rule-Based Bot (Cấp độ 1) khớp từ khóa if/else cố định, không sử dụng LLM.
    """
    print(f"\n🤖 [RULE-BASED BOT] Câu hỏi: {user_query}")
    query_lower = user_query.lower()

    if "chào" in query_lower or "hi" in query_lower:
        ans = "Xin chào! Tôi là Rule-Based Bot (Cấp độ 1). Tôi chỉ có thể trả lời các câu hỏi cố định được lập trình sẵn."
    elif "python" in query_lower:
        ans = "Khóa học Python cơ bản: Mã môn CS101, 3 tín chỉ, học phí cố định."
    elif "thời tiết" in query_lower:
        ans = "Tôi là Bot khớp luật if/else cố định, không thể xem thông tin thời tiết thời gian thực!"
    else:
        ans = "⚠️ LỖI (Rule-Based Bot): Câu hỏi nằm ngoài tập từ khóa/luật cố định được cài đặt sẵn!"

    print(f"🤖 Bot trả lời:\n{ans}")


def run_baseline_chatbot(user_query: str, provider):
    """
    Dựng Chatbot gốc (Baseline) không có công cụ.
    """
    print(f"\n💬 [CHATBOT BASELINE] Câu hỏi: {user_query}")
    print(f"⚙️ System Prompt: {CHATBOT_BASELINE_PROMPT.strip()}")
    
    # Gọi LLM Provider thực hiện sinh câu trả lời
    response = provider.generate(user_query, system_prompt=CHATBOT_BASELINE_PROMPT)
    print(f"🤖 Chatbot trả lời:\n{response}")


def execute_tool_call(action_str: str) -> str:
    """Trích xuất tên công cụ và tham số từ chuỗi Action để thực thi an toàn"""
    match = re.search(r'(\w+)\[(.*?)\]', action_str)
    if not match:
        match = re.search(r'(\w+)\((.*?)\)', action_str)
    if not match:
        return f"LỖI: Không thể phân tích cú pháp Action: '{action_str}'"

    tool_name = match.group(1).strip()
    raw_args = match.group(2).strip()

    args = []
    if raw_args:
        try:
            parsed = ast.literal_eval(f"({raw_args})")
            if isinstance(parsed, tuple):
                args = list(parsed)
            else:
                args = [parsed]
        except Exception:
            args = [a.strip().strip("'\"") for a in raw_args.split(",")]

    if tool_name not in AVAILABLE_TOOLS:
        return f"LỖI: Công cụ '{tool_name}' không tồn tại trong AVAILABLE_TOOLS."

    try:
        tool_func = AVAILABLE_TOOLS[tool_name]
        result = tool_func(*args)
        return str(result)
    except Exception as e:
        return f"LỖI THỰC THI TOOL: {str(e)}"


def run_react_agent(user_query: str, provider):
    """
    Dựng vòng lặp ReAct Agent (Thought -> Action -> Observation) thực tế có Guardrails.
    """
    print(f"\n🤖 [REACT AGENT] Câu hỏi: {user_query}")
    step = 0
    conversation_history = f"Câu hỏi của sinh viên: {user_query}\n"

    while step < MAX_ITERATIONS:
        step += 1
        print(f"\n--- 🔄 Vòng lặp ReAct (Step {step}/{MAX_ITERATIONS}) ---")
        time.sleep(1.5)

        # Gọi LLM sinh bước suy luận/hành động tiếp theo
        response = provider.generate(conversation_history, system_prompt=REACT_SYSTEM_PROMPT).strip()
        print(response)

        # 1. Kiểm tra nếu Agent trả về Final Answer
        if "Final Answer:" in response:
            print("\n✅ ReAct Agent đã hoàn thành nhiệm vụ!")
            break

        # 2. Kiểm tra nếu Agent yêu cầu Action (gọi công cụ)
        if "Action:" in response:
            action_line = [line for line in response.split("\n") if line.startswith("Action:")][0]
            action_str = action_line.replace("Action:", "").strip()

            # Thực thi tool
            obs = execute_tool_call(action_str)
            print(f"👁️ Observation: {obs}")

            # Cập nhật lịch sử hội thoại cho bước lặp tiếp theo
            conversation_history += f"\n{response}\nObservation: {obs}\n"
        else:
            conversation_history += f"\n{response}\n"

    if step >= MAX_ITERATIONS and "Final Answer:" not in response:
        print(f"\n🛡️ GUARDRAIL TRIGGERED: Đã đạt giới hạn tối đa {MAX_ITERATIONS} bước. Ngắt lặp an toàn!")


def run_autonomous_agent(goal_query: str, provider):
    """
    Dựng Autonomous Agent (Cấp độ 4) có khả năng Planning (Rã mục tiêu),
    Lưu bộ nhớ (Memory), Tự đánh giá (Goal Evaluation) và thực thi chuỗi tác vụ.
    """
    print(f"\n🚀 [AUTONOMOUS AGENT - CẤP 4] Mục tiêu phức tạp: {goal_query}")
    memory = []

    # 1. PLANNING: Tự rã mục tiêu lớn thành các sub-goals
    planning_prompt = f"""Bạn là Autonomous Agent Planner. Hãy rã mục tiêu lớn dưới đây thành đúng 3 bước thực thi cụ thể cho sinh viên:
Mục tiêu: {goal_query}

Trả về danh sách 3 bước ngắn gọn theo đúng định dạng:
Bước 1: <tên bước 1>
Bước 2: <tên bước 2>
Bước 3: <tên bước 3>"""

    plan_response = provider.generate(planning_prompt).strip()
    print(f"\n📋 [PLANNING - TỰ RÃ MỤC TIÊU]:\n{plan_response}")

    sub_tasks = [line.strip() for line in plan_response.split("\n") if line.strip().startswith("Bước")]
    if not sub_tasks:
        sub_tasks = [
            "Bước 1: Tra cứu thông tin mã môn học và điều kiện tiên quyết",
            "Bước 2: Tra cứu lịch học và hạn đăng ký tín chỉ",
            "Bước 3: Tổng hợp lập kế hoạch lộ trình học tập trọn gói"
        ]

    # 2. EXECUTION LOOP WITH MEMORY (Thực thi và lưu vết bộ nhớ)
    for idx, task in enumerate(sub_tasks, 1):
        print(f"\n--- 🎯 Thực thi Sub-Goal {idx}/{len(sub_tasks)}: {task} ---")
        time.sleep(1.5)

        memory_context = "\n".join([f"- Step {item['step']}: {item['task']} -> Kết quả: {item['result']}" for item in memory])

        step_prompt = f"""Bộ nhớ lịch sử (Memory):
{memory_context if memory_context else 'Chưa có'}

Nhiệm vụ bước này: {task}
Mục tiêu chung: {goal_query}

Hãy đưa ra suy luận và chỉ định Action gọi công cụ nếu cần (ví dụ: search_courses["Python", "Công nghệ thông tin"] hoặc get_registration_deadlines["HK2024-2025"])."""

        step_output = provider.generate(step_prompt, system_prompt=REACT_SYSTEM_PROMPT).strip()
        print(f"🧠 [Agent Reasoning & Action]:\n{step_output}")

        result_text = step_output
        if "Action:" in step_output:
            action_line = [line for line in step_output.split("\n") if line.startswith("Action:")][0]
            action_str = action_line.replace("Action:", "").strip()
            obs = execute_tool_call(action_str)
            print(f"👁️ [Observation]: {obs}")
            result_text += f" | Observation: {obs}"

        # 3. SAVE TO MEMORY
        memory.append({"step": idx, "task": task, "result": result_text})
        print(f"💾 [Memory Saved]: Đã lưu kết quả Step {idx} vào bộ nhớ.")

    # 4. GOAL EVALUATION & FINAL MASTER PLAN
    print("\n🎯 [GOAL EVALUATION]: Tất cả Sub-goals đã được thực thi hoàn tất!")
    synthesis_prompt = f"""Dựa trên bộ nhớ lịch sử thực thi (Memory):
{json.dumps(memory, ensure_ascii=False, indent=2)}

Hãy tổng hợp Báo cáo Lộ trình Tư vấn Khóa học Trọn gói hoàn chỉnh gửi sinh viên."""

    final_plan = provider.generate(synthesis_prompt).strip()
    print(f"\n🏁 [AUTONOMOUS AGENT - FINAL MASTER PLAN]:\n{final_plan}")


if __name__ == "__main__":
    print("==================================================")
    print("🏫 ĐẠI HỌC VINUNI - BÀI LAB 3: CHATBOT VS REACT AGENT")
    print("==================================================")
    
    # Khởi tạo Multi-Provider LLM Adapter (Đọc từ biến môi trường LLM_PROVIDER)
    provider = get_llm_provider()
    model_name = getattr(provider, "model_name", "Offline Mock Mode")
    print(f"🔌 LLM Provider đang hoạt động: {provider.__class__.__name__} (Model: {model_name})")
    
    tests = load_test_cases()
    print(f"✅ Đã tải thành công {len(tests)} Test Cases từ config/test_cases.json\n")
    
    # Câu test số 3
    sample_query = tests[4]["question"]
    
    print("==================================================")
    print("--- DEMO CẤP ĐỘ 1: RULE-BASED BOT (Khớp từ khóa if/else, Không dùng LLM) ---")
    print("==================================================")
    run_rule_based_bot(sample_query)

    print("\n==================================================")
    print("--- DEMO CẤP ĐỘ 2: LLM CHATBOT BASELINE (Dùng LLM, Không dùng Tool) ---")
    print("==================================================")
    run_baseline_chatbot(sample_query, provider)
    
    print("\n==================================================")
    print("--- DEMO CẤP ĐỘ 3: REACT AGENT (Suy luận Thought -> Action -> Observation) ---")
    print("==================================================")
    run_react_agent(sample_query, provider)

    print("\n==================================================")
    print("--- DEMO CẤP ĐỘ 4: AUTONOMOUS AGENT (Planning, Memory & Goal Evaluation) ---")
    print("==================================================")
    goal_sample = "Lập lộ trình đăng ký học phần trọn gói để sinh viên trở thành Data Engineer trong học kỳ HK2024-2025"
    run_autonomous_agent(goal_sample, provider)
