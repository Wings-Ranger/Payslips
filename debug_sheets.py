#!/usr/bin/env python3
import pandas as pd
from openpyxl import load_workbook

# Read the CSV to understand data types
df = pd.read_csv('output/payslips.csv')
print("=== DATA TYPES ===")
print(df.dtypes)
print(f"\nTotal rows: {len(df)}")
print(f"\ngross_this_pay column:")
print(df['gross_this_pay'].head(10))
print(f"\nnet_this_pay column:")
print(df['net_this_pay'].head(10))
print(f"\ntotal_hours_this_pay column:")
print(df['total_hours_this_pay'].head(10))

# Check for NaN
print(f"\nNaN count by column:")
print(df.isnull().sum())

# Check what create_summary_sheet returns
from pathlib import Path
import sys
sys.path.insert(0, str(Path.cwd() / 'src'))
from payslip_tracker import create_summary_sheet, create_monthly_breakdown, create_weekly_summary

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
