"""
🛠️ TOOL REGISTRY & SCHEMAS (Dành cho Role 2: Tool & Spec Engineer)
Nơi khai báo tất cả các "món đồ nghề" mà ReAct Agent có thể gọi.
"""

import datetime

# ==========================================
# 🗄️ DATABASE SCHEMA & MOCK DATA (MOCK_DB)
# ==========================================
# Cấu trúc Database mô phỏng hệ thống Quản lý Đào tạo Đại học:
# 1. courses: Danh mục khóa học & môn học tiên quyết
# 2. schedules: Thời khóa biểu theo môn và học kỳ
# 3. students: Bảng điểm, ngành học & GPA của sinh viên
# 4. degree_requirements: Khung chương trình đào tạo chuẩn theo ngành
# 5. registration_deadlines: Thời hạn đăng ký/hủy học phần theo học kỳ

MOCK_DATABASE = {
    "courses": {
        "CS101": {
            "course_code": "CS101",
            "name": "Nhập môn Lập trình Python",
            "credits": 3,
            "department": "Công nghệ thông tin",
            "description": "Cung cấp kiến thức cơ bản về lập trình, cú pháp Python, cấu trúc dữ liệu cơ bản.",
            "prerequisites": []
        },
        "CS102": {
            "course_code": "CS102",
            "name": "Cấu trúc dữ liệu và Giải thuật",
            "credits": 4,
            "department": "Công nghệ thông tin",
            "description": "Nghiên cứu các cấu trúc dữ liệu nâng cao (Array, LinkList, Tree, Graph) và thuật toán sắp xếp/tìm kiếm.",
            "prerequisites": ["CS101"]
        },
        "AI201": {
            "course_code": "AI201",
            "name": "Nhập môn Trí tuệ Nhân tạo & Machine Learning",
            "credits": 3,
            "department": "Khoa học Dữ liệu",
            "description": "Học về các thuật toán học máy, ReAct Agent, Neural Networks và ứng dụng thực tế.",
            "prerequisites": ["CS102", "MATH101"]
        },
        "MATH101": {
            "course_code": "MATH101",
            "name": "Đại số tuyến tính & Giải tích cho AI",
            "credits": 3,
            "department": "Toán ứng dụng",
            "description": "Trang bị nền tảng toán học về Ma trận, Vector, Đạo hàm cho Trí tuệ nhân tạo.",
            "prerequisites": []
        },
        "SE301": {
            "course_code": "SE301",
            "name": "Kỹ thuật Phần mềm nâng cao",
            "credits": 3,
            "department": "Công nghệ thông tin",
            "description": "Thiết kế kiến trúc hệ thống, Microservices và quy trình phát triển phần mềm.",
            "prerequisites": ["CS102"]
        }
    },
    "schedules": {
        "CS101_HK2024-2025": {
            "course_code": "CS101",
            "semester": "HK2024-2025",
            "day_of_week": "Thứ 2 & Thứ 4",
            "time": "08:00 - 10:30",
            "room": "Phòng A101 - Giảng đường VinUni",
            "lecturer": "TS. Nguyễn Văn A"
        },
        "CS102_HK2024-2025": {
            "course_code": "CS102",
            "semester": "HK2024-2025",
            "day_of_week": "Thứ 3 & Thứ 5",
            "time": "13:30 - 16:00",
            "room": "Phòng B204 - Giảng đường VinUni",
            "lecturer": "PGS.TS. Trần Thị B"
        },
        "AI201_HK2024-2025": {
            "course_code": "AI201",
            "semester": "HK2024-2025",
            "day_of_week": "Thứ 6",
            "time": "09:00 - 12:00",
            "room": "Phòng AI Lab C305",
            "lecturer": "GS. Lê Hoàng C"
        }
    },
    "students": {
        "SV2024-2025": {
            "student_id": "SV2024-2025",
            "full_name": "Nguyễn Văn Sinh Viên",
            "major_code": "CS",
            "major_name": "Khoa học Máy tính",
            "gpa": 3.6,
            "academic_year": "2023-2027",
            "completed_courses": {
                "CS101": {"grade": "A", "score": 4.0, "semester": "HK2023-1"},
                "MATH101": {"grade": "B+", "score": 3.5, "semester": "HK2023-2"}
            }
        },
        "SV2024001": {
            "student_id": "SV2024001",
            "full_name": "Trần Thị Mai",
            "major_code": "AI",
            "major_name": "Trí tuệ Nhân tạo",
            "gpa": 3.8,
            "academic_year": "2023-2027",
            "completed_courses": {
                "CS101": {"grade": "A", "score": 4.0, "semester": "HK2023-1"},
                "CS102": {"grade": "A-", "score": 3.7, "semester": "HK2023-2"},
                "MATH101": {"grade": "A", "score": 4.0, "semester": "HK2023-2"}
            }
        }
    },
    "degree_requirements": {
        "CS": {
            "major_code": "CS",
            "major_name": "Khoa học Máy tính (Computer Science)",
            "total_credits_required": 130,
            "core_courses": ["CS101", "CS102", "MATH101", "SE301"],
            "elective_courses": ["AI201"],
            "minimum_gpa": 2.0
        },
        "AI": {
            "major_code": "AI",
            "major_name": "Trí tuệ Nhân tạo (Artificial Intelligence)",
            "total_credits_required": 135,
            "core_courses": ["CS101", "CS102", "MATH101", "AI201"],
            "elective_courses": ["SE301"],
            "minimum_gpa": 2.5
        }
    },
    "registration_deadlines": {
        "HK2024-2025": {
            "semester": "HK2024-2025",
            "registration_start": "2026-08-01",
            "registration_end": "2026-08-15",
            "drop_deadline": "2026-08-30",
            "status": "Đang mở cổng đăng ký tín chỉ"
        },
        "HK2025-1": {
            "semester": "HK2025-1",
            "registration_start": "2026-12-01",
            "registration_end": "2026-12-15",
            "drop_deadline": "2026-12-30",
            "status": "Chưa đến thời hạn"
        }
    }
}


def search_courses(query: str, department: str = None) -> dict:
    '''
    Tìm kiếm khóa học dựa trên từ khóa và chuyên ngành.

    Args:
        query (str): Từ khóa tìm kiếm (Ví dụ: 'Python', 'Machine Learning')
        department (str, optional): Chuyên ngành (Ví dụ: 'Công nghệ thông tin'). Defaults to None.
        
    Returns:
        dict: Danh sách khóa học tìm được
    '''
    try:
        query_lower = query.lower()
        matched_courses = []
    
        for code, course in MOCK_DATABASE["courses"].items():
            is_match = (
                query_lower in course["course_code"].lower()
                or query_lower in course["name"].lower()
                or query_lower in course["description"].lower()
            )
            
            if is_match and department:
                if department.lower() not in course["department"].lower():
                    is_match = False
                    
            if is_match:
                matched_courses.append(course)
            
        if not matched_courses:
            return {
                "status": "error",
                "message": f"Không tìm thấy khóa học nào phù hợp với từ khóa '{query}'" + (f" thuộc ngành '{department}'" if department else "")
            }
        
        return {
            "status": "success",
            "total_results": len(matched_courses),
            "courses": matched_courses
        }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Lỗi khi tìm kiếm khóa học: {str(e)}"
            }


def get_course_details(course_code: str) -> dict:
    '''
    Lấy thông tin chi tiết của một khóa học cụ thể.

    Args:
        course_code (str): Mã khóa học (Ví dụ: 'CS101')
        
    Returns:
        dict: Thông tin chi tiết khóa học
    '''
    try: 
        code_upper = course_code.strip().upper()
        course = MOCK_DATABASE["courses"].get(code_upper)
    
        if not course:
            return {
                "status": "error",
                "message": f"Không tìm thấy thông tin cho mã khóa học '{course_code}' trong cơ sở dữ liệu."
            }
        
        return {
            "status": "success",
            "course_details": course
        }
    
    except Exception as e:
        return {
            "status": "error",
            "message": f"Lỗi khi lấy thông tin chi tiết khóa học: {str(e)}"
        }


def get_course_schedule(course_code: str, semester: str) -> dict:
    '''
    Lấy lịch học của một khóa học cụ thể.

    Args:
        course_code (str): Mã khóa học (Ví dụ: 'CS101')
        semester (str): Học kỳ (Ví dụ: 'HK2024-2025')
        
    Returns:
        dict: Lịch học chi tiết khóa học
    '''
    try: 
        key = f"{course_code.strip().upper()}_{semester.strip()}"
        schedule = MOCK_DATABASE["schedules"].get(key)
    
        if not schedule:
            return {
            "status": "error",
            "message": f"Không tìm thấy lịch học cho môn '{course_code}' trong học kỳ '{semester}'."
            }
        
        return {
            "status": "success",
            "schedule": schedule
        }
    
    except Exception as e:
        return {
            "status": "error",
            "message": f"Lỗi khi lấy lịch học: {str(e)}"
        }


def get_student_transcript(student_id: str) -> dict:
    '''
    Lấy bảng điểm của một sinh viên cụ thể.

    Args:
        student_id (str): Mã sinh viên (Ví dụ: 'SV2024-2025')
        
    Returns:
        dict: Bảng điểm chi tiết sinh viên
    '''
    try:
        sid = student_id.strip()
        student = MOCK_DATABASE["students"].get(sid)
    
        if not student:
            return {
                "status": "error",
                "message": f"Không tìm thấy dữ liệu sinh viên có mã '{student_id}'."
            }
        
        return {
            "status": "success",
            "student_info": {
            "student_id": student["student_id"],
            "full_name": student["full_name"],
            "major": student["major_name"],
            "gpa": student["gpa"]
        },
        "transcript": student["completed_courses"]
    }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Lỗi khi lấy bảng điểm: {str(e)}"
        }


def get_degree_requirements(major_code: str) -> dict:
    '''
    Lấy khung chương trình đào tạo chuẩn của ngành học mà sinh viên đang theo đuổi

    Args:
        major_code (str): Mã ngành học (Ví dụ: 'CS', 'AI')
        
    Returns:
        dict: Khung chương trình đào tạo chuẩn
    '''
    try: 
        mcode = major_code.strip().upper()
        reqs = MOCK_DATABASE["degree_requirements"].get(mcode)
    
        if not reqs:
            return {
                "status": "error",
                "message": f"Không tìm thấy yêu cầu đào tạo cho mã ngành '{major_code}'."
            }

        return {
            "status": "success",
            "degree_requirements": reqs
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Lỗi khi lấy yêu cầu đào tạo: {str(e)}"
        }


def check_prerequisites_met(student_id: str, course_code: str) -> dict:
    '''
    Kiểm tra điều kiện tiên quyết (prerequisites) của một khóa học đã được đáp ứng chưa

    Args:
        student_id (str): Mã sinh viên (Ví dụ: 'SV2024-2025')
        course_code (str): Mã khóa học (Ví dụ: 'CS102')
        
    Returns:
        dict: Kết quả kiểm tra điều kiện tiên quyết
    '''
    try:
        sid = student_id.strip()
        ccode = course_code.strip().upper()
    
        student = MOCK_DATABASE["students"].get(sid)
        if not student:
            return {
            "status": "error",
            "message": f"Không tìm thấy dữ liệu sinh viên '{student_id}'."
        }
        
        course = MOCK_DATABASE["courses"].get(ccode)
        if not course:
            return {
                "status": "error",
                "message": f"Không tìm thấy môn học '{course_code}'."
            }

        prereqs = course.get("prerequisites", [])
        completed_courses = list(student.get("completed_courses", {}).keys())
    
        missing_prereqs = [p for p in prereqs if p not in completed_courses]
        is_met = len(missing_prereqs) == 0
    
        return {
            "status": "success",
            "student_id": sid,
            "course_code": ccode,
            "required_prerequisites": prereqs,
            "completed_prerequisites": [p for p in prereqs if p in completed_courses],
            "missing_prerequisites": missing_prereqs,
            "prerequisites_met": is_met,
            "message": "Đủ điều kiện tiên quyết để đăng ký môn học." if is_met else f"Chưa đủ điều kiện! Còn thiếu môn tiên quyết: {', '.join(missing_prereqs)}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Lỗi khi kiểm tra điều kiện tiên quyết: {str(e)}"
        }


def get_registration_deadlines(semester: str) -> dict:
    '''
    Cung cấp thông tin về thời gian mở/đóng cổng đăng ký tín chỉ, thời hạn hủy môn.

    Args:
        semester (str): Học kỳ (Ví dụ: 'HK2024-2025')
        
    Returns:
        dict: Hạn chót đăng ký học phần
    '''
    try:
        sem = semester.strip()
        deadlines = MOCK_DATABASE["registration_deadlines"].get(sem)
    
        if not deadlines:
            return {
                "status": "error",
            "message": f"Không tìm thấy lịch đăng ký cho học kỳ '{semester}'."
        }
        
        return {
            "status": "success",
            "registration_deadlines": deadlines
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Lỗi khi kiểm tra điều kiện tiên quyết: {str(e)}"
        }



# Danh sách các tool được đăng ký để Agent sử dụng
AVAILABLE_TOOLS = {
    "search_courses": search_courses,
    "get_course_details": get_course_details,
    "get_course_schedule": get_course_schedule,
    "get_student_transcript": get_student_transcript,
    "get_degree_requirements": get_degree_requirements,
    "check_prerequisites_met": check_prerequisites_met,
    "get_registration_deadlines": get_registration_deadlines
}

