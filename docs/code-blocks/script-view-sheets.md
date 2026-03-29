# script: view_sheets.py

**File:** `scripts/view_sheets.py`

## What It Is

A developer utility that opens `output/payslips.xlsx` and dumps the raw cell values from four named sheets (`summary`, `monthly`, `weekly`, `deductions`) to the console. It is used to quickly verify that optional summary sheets were created with the expected structure and values after a run.

## Code Block

```python
#!/usr/bin/env python3
from openpyxl import load_workbook

wb = load_workbook("output/payslips.xlsx")

print("=== SUMMARY SHEET ===")
ws = wb["summary"]
for row in ws.iter_rows(values_only=True):
    print(row)

print("\n=== MONTHLY SHEET ===")
ws = wb["monthly"]
for row in ws.iter_rows(values_only=True):
    print(row)

print("\n=== WEEKLY SHEET ===")
ws = wb["weekly"]
for row in ws.iter_rows(values_only=True):
    print(row)

print("\n=== DEDUCTIONS SHEET ===")
ws = wb["deductions"]
for row in ws.iter_rows(values_only=True):
    print(row)

print("\nAll sheets:", wb.sheetnames)
```

## How to Re-Implement

1. Use `load_workbook(path)` from `openpyxl` to open the file without needing Excel installed.
2. Access sheets by name with `wb["sheet_name"]`.
3. `ws.iter_rows(values_only=True)` yields rows as plain tuples of Python values (strings, numbers, dates) rather than `Cell` objects — easier for quick inspection.
4. Run from the project root: `python scripts/view_sheets.py`.

> **Note:** The `summary`, `monthly`, `weekly`, and `deductions` sheets referenced here are not produced by the current version of `run()` — only `payslips` and `missing_weeks` are written. Running this script against the current output will raise a `KeyError`. These sheet names are placeholders for planned future features (aggregated summaries and deduction breakdowns). Once `run()` is extended to write those sheets, this script can be used as-is to verify their contents.

### Adapting for current sheets

```python
wb = load_workbook("output/payslips.xlsx")

print("=== PAYSLIPS SHEET ===")
for row in wb["payslips"].iter_rows(values_only=True):
    print(row)

print("\n=== MISSING WEEKS SHEET ===")
for row in wb["missing_weeks"].iter_rows(values_only=True):
    print(row)
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
