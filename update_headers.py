#!/usr/bin/env python3
"""Add human-readable headers to Excel output."""

import re

# Read the current file
with open('src/payslip_tracker.py', 'r') as f:
    content = f.read()

# Add the header mapping and rename function before the run() function
header_mapping = '''

# Mapping of backend field names to human-readable Excel headers
EXCEL_HEADERS = {
    "file_name": "File Name",
    "employee": "Employee",
    "pay_date": "Pay Date",
    "pay_period": "Pay Period",
    "week_start": "Week Start",
    "ordinary_hours": "Ordinary Hours",
    "ordinary_rate": "Ordinary Rate",
    "ordinary_pay_this": "Ordinary Pay (This)",
    "ordinary_pay_ytd": "Ordinary Pay (YTD)",
    "weekend_hours": "Weekend Hours",
    "weekend_rate": "Weekend Rate",
    "weekend_pay_this": "Weekend Pay (This)",
    "weekend_pay_ytd": "Weekend Pay (YTD)",
    "public_holiday_hours": "Public Holiday Hours",
    "public_holiday_rate": "Public Holiday Rate",
    "public_holiday_pay_this": "Public Holiday Pay (This)",
    "public_holiday_pay_ytd": "Public Holiday Pay (YTD)",
    "gross_this_pay": "Gross Pay (This)",
    "gross_ytd": "Gross Pay (YTD)",
    "tax_this_pay": "Tax (This)",
    "tax_ytd": "Tax (YTD)",
    "payg_this_pay": "PAYG (This)",
    "payg_ytd": "PAYG (YTD)",
    "net_this_pay": "Net Pay (This)",
    "net_ytd": "Net Pay (YTD)",
    "total_hours_this_pay": "Total Hours",
    "notes": "Notes",
}


def rename_for_excel(df: pd.DataFrame) -> pd.DataFrame:
    """Rename dataframe columns to human-readable headers for Excel output."""
    rename_map = {col: EXCEL_HEADERS.get(col, col) for col in df.columns}
    return df.rename(columns=rename_map)

'''

# Find where to insert (before run() function)
run_pos = content.find('def run() -> None:')
if run_pos == -1:
    print("ERROR: Could not find run() function")
    exit(1)

# Insert the header mapping before run()
content = content[:run_pos] + header_mapping + content[run_pos:]

# Now replace the Excel writing calls
# Replace: df.to_excel(writer, index=False, sheet_name="payslips")
# With: df_excel = rename_for_excel(df); df_excel.to_excel(writer, index=False, sheet_name="payslips")

content = re.sub(
    r'(\s+)df\.to_excel\(writer, index=False, sheet_name="payslips"\)',
    r'\1# Rename columns to human-readable headers\n\1df_excel = rename_for_excel(df)\n\1df_excel.to_excel(writer, index=False, sheet_name="payslips")',
    content
)

# Replace missing_weeks header 
content = re.sub(
    r'pd\.DataFrame\(\{"missing_week_start": missing_weeks\}\)\.to_excel\(\s+writer, index=False, sheet_name="missing_weeks"\s+\)',
    r'pd.DataFrame({"missing_week_start": missing_weeks}).to_excel(\n                writer, index=False, sheet_name="missing_weeks", header=["Week Start"]\n            )',
    content
)

# Write the updated content
with open('src/payslip_tracker.py', 'w') as f:
    f.write(content)

print("✓ Successfully updated headers in payslip_tracker.py")
