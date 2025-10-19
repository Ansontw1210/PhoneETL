# utils/regex_helper.py
import re

def is_valid_phone_number(phone: str) -> bool:
    pattern = r"^09\d{8}$"
    return bool(re.match(pattern, phone))
