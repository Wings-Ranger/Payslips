#!/usr/bin/env python3
from pathlib import Path
import sys
sys.path.insert(0, str(Path.cwd() / 'src'))

from payslip_tracker import read_text_from_file

# Read the sample payslip
file_path = Path("input/sample_payslip_25032026.txt")
text = read_text_from_file(file_path)

lines = text.splitlines()
print(f"Total lines: {len(lines)}\n")

for i, line in enumerate(lines):
    print(f"Line {i:2d}: '{line}'")
    if i >= 24:
        break
