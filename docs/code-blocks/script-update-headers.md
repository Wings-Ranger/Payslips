# script: update_headers.py

**File:** `scripts/update_headers.py`

## What It Is

A one-time migration script that was used to add the `EXCEL_HEADERS` dict and `rename_for_excel()` function to `payslip_tracker.py`, and to update the `ExcelWriter` calls to use the renamed columns. It performs in-place regex-based text surgery on the source file.

> **Note:** This script has already been applied — the mapping and function it inserts are now present in `payslip_tracker.py`. It is kept in the repository for reference and as a pattern for future automated code migrations.

## Code Block

```python
#!/usr/bin/env python3
"""Add human-readable headers to Excel output."""

import re

# Read the current source file
with open("src/payslip_tracker.py", "r") as f:
    content = f.read()

# The code block to insert before run()
header_mapping = '''

# Mapping of backend field names to human-readable Excel headers
EXCEL_HEADERS = {
    "file_name": "File Name",
    # ... (full mapping) ...
    "notes": "Notes",
}


def rename_for_excel(df):
    """Rename dataframe columns to human-readable headers for Excel output."""
    rename_map = {col: EXCEL_HEADERS.get(col, col) for col in df.columns}
    return df.rename(columns=rename_map)

'''

# Find insertion point
run_pos = content.find("def run() -> None:")
if run_pos == -1:
    print("ERROR: Could not find run() function")
    exit(1)

content = content[:run_pos] + header_mapping + content[run_pos:]

# Replace raw df.to_excel calls with rename_for_excel(df).to_excel
content = re.sub(
    r"(\s+)df\.to_excel\(writer, index=False, sheet_name=\"payslips\"\)",
    r"\1# Rename columns to human-readable headers\n\1df_excel = rename_for_excel(df)\n\1df_excel.to_excel(writer, index=False, sheet_name=\"payslips\")",
    content,
)

# Update missing_weeks header parameter
content = re.sub(
    r'pd\.DataFrame\(\{"missing_week_start": missing_weeks\}\)\.to_excel\(\s+writer, index=False, sheet_name="missing_weeks"\s+\)',
    r'pd.DataFrame({"missing_week_start": missing_weeks}).to_excel(\n                writer, index=False, sheet_name="missing_weeks", header=["Week Start"]\n            )',
    content,
)

with open("src/payslip_tracker.py", "w") as f:
    f.write(content)

print("✓ Successfully updated headers in payslip_tracker.py")
```

## How to Re-Implement

This pattern is useful whenever you need to programmatically insert or replace code in a Python source file as part of a migration:

1. Read the entire file into a string.
2. Locate the insertion point using `str.find()` or `re.search()`.
3. Perform string slicing or `re.sub()` to insert/replace the target block.
4. Write the modified string back to the file.
5. Verify the change by running the modified module's tests.

### Key cautions

- Always take a backup or commit the file before running a migration script.
- Use narrow `re.sub()` patterns to avoid unintended replacements.
- Guard against the insertion point not being found (check `run_pos == -1`).
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
