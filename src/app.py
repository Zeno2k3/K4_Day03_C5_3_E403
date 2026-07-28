"""
🚀 CORE AGENT APP (Dành cho Role 4: Core Agent Developer)
File chính ghép nối tất cả các thành phần: Tools + Prompts + Test Cases + Multi-Provider.
"""

import ast
import json
import os
import re
import sys
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
    
    # Chạy thử câu test số 3
    sample_query = tests[2]["question"]
    
    print("--- DEMO 1: CHẠY TRÊN CHATBOT BASELINE ---")
    run_baseline_chatbot(sample_query, provider)
    
    print("\n--- DEMO 2: CHẠY TRÊN REACT AGENT ---")
    run_react_agent(sample_query, provider)
