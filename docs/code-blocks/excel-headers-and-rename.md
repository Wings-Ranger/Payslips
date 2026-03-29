# EXCEL_HEADERS and rename_for_excel

**File:** `src/payslip_tracker.py`

## What It Is

`EXCEL_HEADERS` is a dict that maps every backend field name (snake_case, as stored in the DataFrame and CSV) to a human-readable column header used in the Excel workbook. `rename_for_excel` applies that mapping to a DataFrame's columns.

Keeping the mapping in one place means the CSV always uses machine-friendly names while the spreadsheet always shows human-friendly labels, with a single source of truth for the translation.

## Code Block

```python
import pandas as pd

EXCEL_HEADERS = {
    "file_name":               "File Name",
    "employee":                "Employee",
    "pay_date":                "Pay Date",
    "pay_period":              "Pay Period",
    "week_start":              "Week Start",
    "ordinary_hours":          "Ordinary Hours",
    "ordinary_rate":           "Ordinary Rate",
    "ordinary_pay_this":       "Ordinary Pay (This)",
    "ordinary_pay_ytd":        "Ordinary Pay (YTD)",
    "weekend_hours":           "Weekend Hours",
    "weekend_rate":            "Weekend Rate",
    "weekend_pay_this":        "Weekend Pay (This)",
    "weekend_pay_ytd":         "Weekend Pay (YTD)",
    "public_holiday_hours":    "Public Holiday Hours",
    "public_holiday_rate":     "Public Holiday Rate",
    "public_holiday_pay_this": "Public Holiday Pay (This)",
    "public_holiday_pay_ytd":  "Public Holiday Pay (YTD)",
    "gross_this_pay":          "Gross Pay (This)",
    "gross_ytd":               "Gross Pay (YTD)",
    "tax_this_pay":            "Tax (This)",
    "tax_ytd":                 "Tax (YTD)",
    "payg_this_pay":           "PAYG (This)",
    "payg_ytd":                "PAYG (YTD)",
    "net_this_pay":            "Net Pay (This)",
    "net_ytd":                 "Net Pay (YTD)",
    "total_hours_this_pay":    "Total Hours",
    "notes":                   "Notes",
}


def rename_for_excel(df: pd.DataFrame) -> pd.DataFrame:
    """Rename dataframe columns to human-readable headers for Excel output."""
    rename_map = {col: EXCEL_HEADERS.get(col, col) for col in df.columns}
    return df.rename(columns=rename_map)
```

## How to Re-Implement

1. Define `EXCEL_HEADERS` as a module-level dict so it can be imported in tests.
2. In `rename_for_excel`, build the rename map dynamically from the DataFrame's actual columns — this means columns absent from `EXCEL_HEADERS` pass through unchanged, and extra columns added in future are handled gracefully.
3. Use `df.rename(columns=rename_map)` which returns a new DataFrame and does not mutate the original.

### Usage

```python
# Keep the machine-readable version for CSV
df.to_csv("output/payslips.csv", index=False)

# Rename for Excel display
df_excel = rename_for_excel(df)
df_excel.to_excel(writer, index=False, sheet_name="payslips")
```

### Checking a header in tests

```python
from payslip_tracker import EXCEL_HEADERS, rename_for_excel

renamed = rename_for_excel(df)
assert EXCEL_HEADERS["net_this_pay"] in renamed.columns  # "Net Pay (This)"
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
