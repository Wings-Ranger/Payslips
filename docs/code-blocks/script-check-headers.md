# script: check_headers.py

**File:** `scripts/check_headers.py`

## What It Is

A developer utility that inspects the most recently written Excel output file and prints its column headers. It is used to verify that `rename_for_excel()` has applied the expected human-readable labels to the `payslips` sheet.

## Code Block

```python
#!/usr/bin/env python3
from openpyxl import load_workbook
import glob

# Find the latest Excel file
excel_files = glob.glob("output/payslips*.xlsx")
if not excel_files:
    print("No Excel files found")
    exit(1)

latest_file = max(excel_files)
print(f"Checking: {latest_file}\n")

wb = load_workbook(latest_file)

# Check payslips sheet headers
if "payslips" in wb.sheetnames:
    ws = wb["payslips"]
    headers = [cell.value for cell in ws[1]]
    print("=== Payslips Sheet Headers ===")
    for i, h in enumerate(headers[:10], 1):
        print(f"{i:2d}. {h}")
    print(f"... ({len(headers)} total columns)")

print(f"\nAll sheets: {wb.sheetnames}")
```

## How to Re-Implement

1. Install `openpyxl`: `pip install openpyxl`.
2. `glob.glob("output/payslips*.xlsx")` matches both `payslips.xlsx` and timestamped backups like `payslips_20260307_120000.xlsx`. `max(...)` selects the lexicographically last one (most recent by name).
3. `ws[1]` returns all cells in the first row (the header row) as a tuple.
4. Run from the project root: `python scripts/check_headers.py`.

### Usage

```
$ python scripts/check_headers.py
Checking: output/payslips.xlsx

=== Payslips Sheet Headers ===
 1. File Name
 2. Employee
 3. Pay Date
 4. Pay Period
 5. Week Start
 6. Ordinary Hours
 7. Ordinary Rate
 8. Ordinary Pay (This)
 9. Ordinary Pay (YTD)
10. Weekend Hours
... (27 total columns)

All sheets: ['payslips', 'missing_weeks']
```
## Beginner Ramp-Up

If this feels advanced, read these first:

- [../building-blocks/implementation-basics.md](../building-blocks/implementation-basics.md)
- [../building-blocks/configuration-and-paths.md](../building-blocks/configuration-and-paths.md)
- [../building-blocks/python-data-models.md](../building-blocks/python-data-models.md)
- [../building-blocks/regex-basics.md](../building-blocks/regex-basics.md)
- [../building-blocks/dataframe-basics.md](../building-blocks/dataframe-basics.md)
- [../building-blocks/testing-basics.md](../building-blocks/testing-basics.md)
- [../building-blocks/tkinter-basics.md](../building-blocks/tkinter-basics.md)

Follow this order: building block -> this file's implementation steps -> tests.

## When This Is Not The Best Fit

- If your requirements are much simpler, prefer a smaller implementation.
- If your input format differs heavily, adapt the pattern rather than copying it exactly.
- If this is a one-time script, consider readability-first code before framework-style structure.
