import unittest
from Modules.text_utils import to_fullwidth, remove_spaces, remove_symbols


class TestTextUtils(unittest.TestCase):

    def test_to_fullwidth_basic(self):
        self.assertEqual(to_fullwidth('ABC 123!'), 'ＡＢＣ　１２３！')

    def test_to_fullwidth_non_ascii(self):
        self.assertEqual(to_fullwidth('測試abc'), '測試ａｂｃ')

    def test_remove_spaces(self):
        self.assertEqual(remove_spaces(' a b\t\nc　d '), 'abcd')

    def test_remove_symbols(self):
        self.assertEqual(remove_symbols('abc, 123。測試！@#'), 'abc123測試')

    def test_none_input(self):
        self.assertIsNone(to_fullwidth(None))
        self.assertIsNone(remove_spaces(None))
        self.assertIsNone(remove_symbols(None))


if __name__ == '__main__':
    unittest.main()
