# Payslip Tracker

Automatically parse payslips, detect missing weeks, and export a spreadsheet.

## Quick Start (Non-Technical)

1. Put your payslip files into the `input` folder.
2. Double-click `run_tracker.bat`.
3. Wait for completion. The spreadsheet opens automatically if created.
4. Find outputs in `output/`:
	- `payslips.xlsx`
	- `payslips.csv`

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
- If `py` is not available on your machine, edit `run_tracker.bat` and replace `py` with `python`.

