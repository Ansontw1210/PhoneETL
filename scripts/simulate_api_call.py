"""Simple script to simulate calling the validation API locally (direct function call).

This script imports `Services.validation_api.validate_phones` and runs it against
`Tests/fixtures/mixed.csv` then prints the summary.
"""
import os
import sys

# ensure project root is on sys.path so top-level packages like Services and Utils are importable
ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from Services.validation_api import validate_phones


def main():
    print("Simulating validation run against Tests/fixtures/mixed.csv")
    summary = validate_phones(fixture='mixed.csv')
    print('Summary:')
    for k, v in summary.items():
        print(f'  {k}: {v}')


if __name__ == '__main__':
    main()
