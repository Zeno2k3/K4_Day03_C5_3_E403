"""
🛠️ TOOL REGISTRY & SCHEMAS (Dành cho Role 2: Tool & Spec Engineer)
Nơi khai báo tất cả các "món đồ nghề" mà ReAct Agent có thể gọi.
"""

import datetime
def get_weather(location: str) -> str:
    """
    Tra cứu thời tiết hiện tại của một thành phố.
    
    Args:
        location (str): Tên thành phố (Ví dụ: 'Hà Nội', 'TP.HCM', 'Đà Nẵng')
        
    Returns:
        str: Thông tin thời tiết chi tiết
    """
    loc_lower = location.lower()
    if "hà nội" in loc_lower or "ha noi" in loc_lower:
        return "Thời tiết Hà Nội: 28°C, Nắng nhẹ, Độ ẩm 65%."
    elif "hồ chí minh" in loc_lower or "tp.hcm" in loc_lower or "hcm" in loc_lower:
        return "Thời tiết TP.HCM: 33°C, Nắng nóng, Có mây."
    elif "đà nẵng" in loc_lower or "da nang" in loc_lower:
        return "Thời tiết Đà Nẵng: 30°C, Gió nhẹ, Mát mẻ."
    else:
        return f"LỖI: Không tìm thấy dữ liệu thời tiết cho địa điểm '{location}'."


def search_flights(origin: str, destination: str) -> str:
    """
    Tra cứu chuyến bay giữa hai địa điểm.
    
    Args:
        origin (str): Nơi đi (Ví dụ: 'TP.HCM')
        destination (str): Nơi đến (Ví dụ: 'Hà Nội')
        
    Returns:
        str: Danh sách chuyến bay khả dụng và giá vé
    """
    return (
        f"Chuyến bay từ {origin} -> {destination} ngày mai:\n"
        f"1. VN123 (08:00) - Giá: 1,500,000 VNĐ (Còn vé)\n"
        f"2. VJ456 (14:30) - Giá: 1,200,000 VNĐ (Còn vé)"
    )

def search_courses(query: str, department: str = None) -> dict:
    
    '''
    Tìm kiếm khóa học dựa trên từ khóa và chuyên ngành.

    Args:
        query (str): Từ khóa tìm kiếm (Ví dụ: 'Python', 'Machine Learning')
        department (str, optional): Chuyên ngành (Ví dụ: 'Công nghệ thông tin'). Defaults to None.
        
    Returns:
        str: Danh sách khóa học tìm được
    '''

    return {}

def get_course_details(course_code: str) -> dict:
    
    '''
    Lấy thông tin chi tiết của một khóa học cụ thể.

    Args:
        course_code (str): Mã khóa học (Ví dụ: 'CS101')
        
    Returns:
        dict: Thông tin chi tiết khóa học
    '''
    return {}


def get_course_schedule(course_code: str, semester: str) -> dict:
    
    '''
    Lấy lịch học của một khóa học cụ thể.

    Args:
        course_code (str): Mã khóa học (Ví dụ: 'CS101')
        semester (str): Học kỳ (Ví dụ: 'HK2024-2025')
        
    Returns:
        dict: Lịch học chi tiết khóa học
    '''
    return {}

def get_student_transcript(student_id: str) -> dict:

    '''
    Lấy bảng điểm của một sinh viên cụ thể.

    Args:
        student_id (str): Mã sinh viên (Ví dụ: 'SV2024-2025')
        
    Returns:
        dict: Bảng điểm chi tiết sinh viên
    '''
    return {}

def get_degree_requirements(major_code: str) -> dict:
    '''
    Lấy khung chương trình đào tạo chuẩn của ngành học mà sinh viên đang theo đuổi

    Args:
        major_code (str): Mã ngành học (Ví dụ: 'CS101')
        
    Returns:
        dict: Khung chương trình đào tạo chuẩn
    '''
    return {}

def check_prerequisites_met(student_id: str, course_code: str) -> bool:
    '''
    Kiểm tra điều kiện tiên quyết (prerequisites) của một khóa học đã được đáp ứng chưa

    Args:
        student_id (str): Mã sinh viên (Ví dụ: 'SV2024-2025')
        course_code (str): Mã khóa học (Ví dụ: 'CS101')
        
    Returns:
        dict: Kết quả kiểm tra điều kiện tiên quyết
    '''
    return True

def get_registration_deadlines(semester: str) -> dict:
    '''
    Cung cấp thông tin về thời gian mở/đóng cổng đăng ký tín chỉ, thời hạn hủy môn.

    Args:
        semester (str): Học kỳ (Ví dụ: 'HK2024-2025')
        
    Returns:
        dict: Hạn chót đăng ký học phần
    '''
    return {}
# Danh sách các tool được đăng ký để Agent sử dụng
AVAILABLE_TOOLS = {
    "get_weather": get_weather,
    "search_flights": search_flights,
}
