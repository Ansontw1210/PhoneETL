import unittest
import csv
import glob
from Utils.regex_helper import is_valid_phone_number
from Services.phone_service import check_phone_availability

class TestCSVValidation(unittest.TestCase):

    def test_fixtures(self):
        files = glob.glob('Tests/fixtures/*.csv')
        self.assertTrue(files, 'No fixture CSV files found')
        for fp in files:
            with open(fp, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    phone = row['phone']
                    expected_valid = row['expected_valid'].strip().lower() == 'true'
                    expected_available = row['expected_available'].strip().lower() == 'true'

                    actual_valid = is_valid_phone_number(phone)
                    self.assertEqual(actual_valid, expected_valid, f"Validity mismatch for {phone} in {fp}")

                    # Only check availability when format is valid
                    if actual_valid:
                        avail, msg = check_phone_availability(phone)
                        self.assertEqual(avail, expected_available, f"Availability mismatch for {phone} in {fp}")

if __name__ == '__main__':
    unittest.main()
