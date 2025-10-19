# services/phone_service.py
from Utils.regex_helper import is_valid_phone_number

def check_phone_availability(phone: str) -> tuple[bool, str]:
    if not is_valid_phone_number(phone):
        return False, "格式錯誤"
    if phone.startswith("0911"):
        return False, "此號碼已被禁止註冊"
    return True, "號碼可用"
