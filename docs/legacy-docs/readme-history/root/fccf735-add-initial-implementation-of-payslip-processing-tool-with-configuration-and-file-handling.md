# Payslip Tracker

Automatically parse payslips, detect missing weeks, and export a spreadsheet.

## What it does

- Scans files in `input/` (`.pdf` and `.txt` by default)
- Extracts values such as pay date, gross/net pay, tax, NI, and hours
- Builds `output/payslips.xlsx` and `output/payslips.csv`
- Prints missing weekly payslips based on detected week starts

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run

```powershell
python src/payslip_tracker.py
```

## Input

Drop payslips into `input/`.

## Notes

- Parsing works best when the PDF text is selectable.
- If your payslip labels differ, update `config.json` under `field_aliases`.

