import unittest
import csv
import glob
import os
import json
import time
from Utils.regex_helper import is_valid_phone_number
from Services.phone_service import check_phone_availability


class TestCSVValidation(unittest.TestCase):

    def test_fixtures(self):
        # Allow overriding fixtures directory via environment variable
        fixtures_dir = os.environ.get('TEST_FIXTURES', 'Tests/fixtures')
        pattern = os.path.join(fixtures_dir, '*.csv')
        files = glob.glob(pattern)
        self.assertTrue(files, f'No fixture CSV files found in {fixtures_dir}')

        results = []
        any_failed = False

        for fp in files:
            with open(fp, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    phone = row['phone']
                    expected_valid = row['expected_valid'].strip().lower() == 'true'
                    expected_available = row['expected_available'].strip().lower() == 'true'

                    actual_valid = None
                    actual_available = None
                    note = ''
                    try:
                        actual_valid = is_valid_phone_number(phone)
                    except Exception as e:
                        note = f'validation-exception: {e}'

                    if actual_valid:
                        try:
                            avail, msg = check_phone_availability(phone)
                            actual_available = bool(avail)
                        except Exception as e:
                            note = f'availability-exception: {e}'

                    passed = (actual_valid == expected_valid) and (not actual_valid or actual_available == expected_available)
                    if not passed:
                        any_failed = True

                    results.append({
                        'fixture': os.path.basename(fp),
                        'phone': phone,
                        'expected_valid': expected_valid,
                        'expected_available': expected_available,
                        'actual_valid': actual_valid,
                        'actual_available': actual_available,
                        'pass': passed,
                        'note': note,
                    })

        # Ensure results directory exists and write a timestamped report
        reports_dir = os.path.join('Tests', 'results')
        os.makedirs(reports_dir, exist_ok=True)
        ts = time.strftime('%Y%m%d-%H%M%S')
        report_path = os.path.join(reports_dir, f'report-{ts}.json')
        with open(report_path, 'w', encoding='utf-8') as rf:
            json.dump({'fixtures_dir': fixtures_dir, 'results': results}, rf, ensure_ascii=False, indent=2)

        # If any row failed, make the test fail and point to report
        if any_failed:
            failed_count = sum(1 for r in results if not r['pass'])
            self.fail(f"{failed_count} fixture checks failed. See {report_path} for details.")


if __name__ == '__main__':
    unittest.main()
