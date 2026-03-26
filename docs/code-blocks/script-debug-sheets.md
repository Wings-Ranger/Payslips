# script: debug_sheets.py

**File:** `scripts/debug_sheets.py`

## What It Is

A developer utility that reads `output/payslips.csv` into a DataFrame, inspects its data types and null counts, and then calls three summary-generation functions (`create_summary_sheet`, `create_monthly_breakdown`, `create_weekly_summary`) to verify their output before writing to Excel. Useful when diagnosing type errors or missing values in the summary sheets.

## Code Block

```python
#!/usr/bin/env python3
import pandas as pd
from openpyxl import load_workbook
from pathlib import Path
import sys

sys.path.insert(0, str(Path.cwd() / "src"))
from payslip_tracker import create_summary_sheet, create_monthly_breakdown, create_weekly_summary

# Read the CSV to understand data types
df = pd.read_csv("output/payslips.csv")
print("=== DATA TYPES ===")
print(df.dtypes)
print(f"\nTotal rows: {len(df)}")
print(f"\ngross_this_pay column:")
print(df["gross_this_pay"].head(10))
print(f"\nnet_this_pay column:")
print(df["net_this_pay"].head(10))
print(f"\ntotal_hours_this_pay column:")
print(df["total_hours_this_pay"].head(10))

print(f"\nNaN count by column:")
print(df.isnull().sum())

print("\n=== SUMMARY SHEET OUTPUT ===")
summary_df = create_summary_sheet(df)
print(summary_df)

print("\n=== MONTHLY BREAKDOWN OUTPUT ===")
monthly_df = create_monthly_breakdown(df)
print(monthly_df)
print(monthly_df.dtypes)

print("\n=== WEEKLY SUMMARY OUTPUT ===")
weekly_df = create_weekly_summary(df)
print(weekly_df)
print(weekly_df.dtypes)
```

## How to Re-Implement

1. Add `src/` to `sys.path` so the import resolves correctly.
2. Use `pd.read_csv()` to read the CSV output — this mirrors what would be loaded if you were resuming a previous run without re-parsing all payslips.
3. Print `.dtypes` and `.isnull().sum()` to check for unexpected object columns or null counts before running aggregation functions.
4. Run from the project root: `python scripts/debug_sheets.py`.

> **⚠ Not runnable in current state:** `create_summary_sheet`, `create_monthly_breakdown`, and `create_weekly_summary` are not present in the current `payslip_tracker.py`. Running this script will raise an `ImportError`. It is kept as a development template for when those aggregation features are added. Once implemented, run from the project root with `python scripts/debug_sheets.py`.
