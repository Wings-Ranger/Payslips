#!/usr/bin/env python3
from pathlib import Path
import sys
sys.path.insert(0, str(Path.cwd() / 'src'))

from payslip_tracker import read_text_from_file, extract_currency_values

# Read the sample payslip
file_path = Path("input/sample_payslip_25032026.txt")
text = read_text_from_file(file_path)

print("=== Processing Sample Payslip ===\n")
in_salary_section = False
for i, line in enumerate(text.splitlines()):
    line_lower = line.lower()
    
    # Track section changes
    if "salary & wages" in line_lower:
        in_salary_section = True
        print(f"Line {i}: Entering salary section")
        continue
    if in_salary_section and ("tax" in line_lower or line_lower.startswith("tax")):
        in_salary_section = False
        print(f"Line {i}: Exiting salary section (line: '{line}')")
    
    if in_salary_section:
        # Check for TOTAL
        if line_lower.strip() == "total":
            parts = extract_currency_values(line)
            print(f"Line {i}: FOUND TOTAL LINE!")
            print(f"  Line text: '{line}'")
            print(f"  line_lower.strip(): '{line_lower.strip()}'")
            print(f"  Extracted values: {parts}")
            print(f"  len(parts): {len(parts)}")
            if len(parts) >= 2:
                print(f"  gross_this_pay would be: {parts[0]}")
                print(f"  gross_ytd would be: {parts[1]}")
        # Check for ordinary
        elif "ordinary hours" in line_lower:
            print(f"Line {i}: Ordinary hours found")
        # Check for weekends
        elif "weekends" in line_lower:
            print(f"Line {i}: Weekends found")
