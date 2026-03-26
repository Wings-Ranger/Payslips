#!/usr/bin/env python3
import re
from pathlib import Path
import sys
sys.path.insert(0, str(Path.cwd() / 'src'))

from payslip_tracker import extract_currency_values, read_text_from_file, parse_payslip, load_config

# Test extract_currency_values function
test_lines = [
    "Ordinary Hours 7.5000 $16.7100 $125.32 $7,337.90",
    "Weekends Sat/Sun 5.0000 $21.8000 $109.00 $4,352.33",
    "TOTAL $234.32 $12,235.23",
    "PAYG $0.00 $264.00",
]

print("=== Testing extract_currency_values ===")
for line in test_lines:
    values = extract_currency_values(line)
    print(f"Line: {line}")
    print(f"  Values: {values}")

# Test on actual file
config = load_config(Path.cwd())
file_path = Path("input/sample_payslip_25032026.txt")
text = read_text_from_file(file_path)
record = parse_payslip(file_path, text, config)

print(f"\n=== Sample Payslip Parsing ===")
print(f"Gross this pay: {record.gross_this_pay}")
print(f"Gross YTD: {record.gross_ytd}")
print(f"Ordinary hours: {record.ordinary_hours}")
print(f"Ordinary rate: {record.ordinary_rate}")
print(f"Net this pay: {record.net_this_pay}")
print(f"Total hours: {record.total_hours_this_pay}")
