# main.py
from Services.phone_service import check_phone_availability

if __name__ == "__main__":
    phone = input("請輸入手機號碼：")
    result, message = check_phone_availability(phone)
    print(message)
