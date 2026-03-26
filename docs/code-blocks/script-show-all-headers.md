# script: show_all_headers.py

**File:** `scripts/show_all_headers.py`

## What It Is

A developer utility that finds the most recently written Excel output file, reads all column headers from the `payslips` sheet, and prints them with their 1-based column index. It also prints a few sample data rows so you can verify that the human-readable headers are correctly aligned with the data.

## Code Block

```python
#!/usr/bin/env python3
from openpyxl import load_workbook
import glob

# Find the latest Excel file that has a payslips sheet
excel_files = glob.glob("output/payslips*.xlsx")
for file in sorted(excel_files, reverse=True):
    try:
        wb = load_workbook(file)
        if "payslips" in wb.sheetnames:
            print(f"Using: {file}\n")

            ws = wb["payslips"]
            headers = [cell.value for cell in ws[1]]
            print("=== Payslips Sheet - All Human-Readable Headers ===\n")
            for i, h in enumerate(headers, 1):
                print(f"{i:2d}. {h}")

            print(f"\n✓ Human-readable headers successfully applied!")
            print(f"✓ Backend field names preserved in CSV (payslips.csv)")

            print(f"\nData samples:")
            for i, row in enumerate(ws.iter_rows(min_row=2, max_row=6, values_only=True), 1):
                print(f"  Row {i}: {row[0]} | {row[2]} | ${row[17]}")
            break
    except Exception:
        continue
```

## How to Re-Implement

1. Use `sorted(..., reverse=True)` combined with a `try/except` to skip corrupt or locked files and always land on the newest valid workbook.
2. `ws[1]` is the header row as a tuple of `Cell` objects; access `.value` to get the text.
3. `ws.iter_rows(min_row=2, max_row=6, values_only=True)` prints up to 5 sample data rows — adjust `max_row` as needed.
4. Run from the project root: `python scripts/show_all_headers.py`.

### Difference from check_headers.py

| Script | Shows | Use when |
|--------|-------|----------|
| `check_headers.py` | First 10 headers + count | Quick sanity check |
| `show_all_headers.py` | All headers + sample data rows | Full verification after a format change |
