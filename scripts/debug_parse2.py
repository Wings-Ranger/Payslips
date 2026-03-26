#!/usr/bin/env python3
from pathlib import Path
import sys
sys.path.insert(0, str(Path.cwd() / 'src'))

from payslip_tracker import read_text_from_file, extract_currency_values

# Read the sample payslip
file_path = Path("input/sample_payslip_25032026.txt")
text = read_text_from_file(file_path)

print("=== Detailed Parsing Debug ===\n")
in_salary_section = False
for i, line in enumerate(text.splitlines()):
    line_lower = line.lower()
    
    print(f"Line {i:2d}: in_section={in_salary_section} | '{line}'")
    
    # Track section changes
    if "salary & wages" in line_lower:
        in_salary_section = True
        print(f"       -> Entering salary section, continue")
        continue
    if in_salary_section and ("tax" in line_lower or line_lower.startswith("tax")):
        in_salary_section = False
        print(f"       -> Exiting salary section")
    
    if in_salary_section:
        if line_lower.strip() == "total":
            parts = extract_currency_values(line)
            print(f"       -> TOTAL line detected! values={parts}")
        elif "ordinary hours" in line_lower:
            print(f"       -> Ordinary hours")
        elif "weekends" in line_lower:
            print(f"       -> Weekends")
        elif line.strip() != "":
            print(f"       -> Other line in salary section")
