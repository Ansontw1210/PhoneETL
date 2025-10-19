# tests/test_phone_utils.py
import unittest
from Utils.regex_helper import is_valid_phone_number
from Services.phone_service import check_phone_availability

class TestPhoneValidation(unittest.TestCase):

    def test_valid_number(self):
        self.assertTrue(is_valid_phone_number("0968123456"))

    def test_invalid_number_format(self):
        self.assertFalse(is_valid_phone_number("12345"))

    def test_banned_number(self):
        result, msg = check_phone_availability("0911888999")
        self.assertFalse(result)
        self.assertEqual(msg, "此號碼已被禁止註冊")

if __name__ == '__main__':
    unittest.main()
