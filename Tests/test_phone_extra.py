import unittest
import time
import os
from Utils.regex_helper import is_valid_phone_number
from Services.phone_service import check_phone_availability

class TestPhoneExtra(unittest.TestCase):

    def test_boundary_min_length(self):
        # 最短合法手機號（符合格式 ^09\d{8}$）
        self.assertTrue(is_valid_phone_number("0900000000"))

    def test_boundary_max_like(self):
        # 另一個合法例子
        self.assertTrue(is_valid_phone_number("0999999999"))

    def test_none_input(self):
        # None 應該被視為無效格式
        with self.assertRaises(TypeError):
            # is_valid_phone_number 期望字符串，傳 None 應拋出 TypeError
            is_valid_phone_number(None)  # type: ignore

    def test_numeric_input(self):
        # 整數輸入不合法
        with self.assertRaises(TypeError):
            is_valid_phone_number(968123456)  # type: ignore

    def test_input_with_spaces_and_dashes(self):
        self.assertFalse(is_valid_phone_number("0968 123 456"))
        self.assertFalse(is_valid_phone_number("0968-123-456"))

    def test_banned_prefixs_variations(self):
        # 確認以 0911 開頭會被禁止
        result, msg = check_phone_availability("0911123456")
        self.assertFalse(result)
        self.assertEqual(msg, "此號碼已被禁止註冊")

    @unittest.skipUnless(os.environ.get('RUN_PERF_TESTS') == '1', 'skip perf by default')
    def test_performance_is_valid(self):
        # 簡單效能測試：測量 10000 次匹配所需時間
        n = 10000
        start = time.time()
        for i in range(n):
            is_valid_phone_number("0968123456")
        duration = time.time() - start
        # 期望 10000 次在 2 秒內（視機器而定，可調整）
        self.assertLess(duration, 2.0)

if __name__ == '__main__':
    unittest.main()
