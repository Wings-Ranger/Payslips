# Payslip Tracker

Automatically parse payslips, detect missing weeks, generate summaries, and create multi-sheet analytics reports.

## Quick Start (Non-Technical)

1. Put your payslip files into the `input` folder.
2. Double-click `run_tracker_fallback.bat` (recommended).
   - It tries `py` first, then `python`.
3. Wait for completion.
4. Find outputs in `output/`:
   - `payslips.xlsx` (multi-sheet report with summaries and analytics)
   - `payslips.csv` (detailed data export)
   - `backups/` (automatic backup with timestamp)

## What it does

- **Scans & Parses**: Reads payslips from `input/` (`.pdf` and `.txt` files)
- **Extracts Data**: Captures 28 fields including:
  - Employee details, pay dates, pay periods
  - Hours: ordinary, weekend, public holiday
  - Pay rates and this-pay amounts
  - Year-to-date (YTD) totals
  - Gross, net, tax, and PAYG amounts
- **Generates Multi-Sheet Excel Report**:
  - **payslips**: All raw payslip data with professional formatting
  - **summary**: Key statistics (totals, averages, YTD figures)
  - **monthly**: Monthly breakdown with aggregated pay and hours
  - **weekly**: Weekly summaries by week start date
  - **deductions**: Tax and PAYG breakdown analysis
  - **missing_weeks**: List of weeks with no payslip detected
  - **alerts**: Anomaly detection for unusual pay or low hours
- **Creates Backups**: Automatic timestamped backup after each run
- **Exports CSV**: Detailed data in CSV format for other tools
- **Detects Issues**: Identifies missing weekly payslips and anomalies

## Output

The tracker generates a professional multi-sheet Excel workbook (`payslips.xlsx`) with the following sheets:

### **payslips** (Raw Data)
- All 28 fields from each payslip in a single table
- Color-coded columns by category (hours, rates, gross, net, tax)
- Frozen header row for easy scrolling
- Formatted with proper number formatting and borders

### **summary** (Key Metrics)
- Total payslips processed
- Date range covered
- **Totals**: Gross pay, net pay, tax, hours worked
- **Averages**: Weekly gross, weekly net, hours per week
- **YTD totals**: Year-to-date figures from latest payslip

### **monthly** (Monthly Breakdown)
- Aggregated by month (YYYY-MM)
- Gross/net/tax per month
- Total hours worked per month
- Number of payslips per month

### **weekly** (Weekly Summary)
- Aggregated by week start date
- Hours by type: ordinary, weekend, public holiday
- Weekly gross/net/tax totals
- Useful for tracking weekly patterns

### **deductions** (Tax Analysis)
- PAYG tax breakdown
- Other tax amounts
- Both this-pay and YTD figures
- Helps track tax withholding trends

### **missing_weeks**
- Lists any weeks with no payslip detected
- Useful for identifying gaps
- Based on week start dates from parsed payslips

### **alerts** (Anomalies)
- Flags weeks with unusually low pay
- Flags weeks with unusually low hours
- Helps identify potential errors or part-time weeks

## Setup

### Option 1: Using Python directly
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python src/payslip_tracker.py
```

### Option 2: Using the bat launcher (Recommended)
```powershell
.\run_tracker_fallback.bat
```

## Input

1. Place payslip files in the `input/` folder
2. Supported formats:
   - **Text PDF files** (recommended) - PDFs with selectable text
   - **Plain text** (`.txt` files) - For testing or manual exports
3. File naming doesn't matter - the tracker processes all supported files

## Configuration

Edit `config.json` to customize behavior:

```json
{
  "input_dir": "input",                    // Where to read payslips from
  "output_dir": "output",                  // Where to save Excel/CSV
  "output_filename": "payslips.xlsx",      // Name of output file
  "supported_extensions": [".pdf", ".txt"], // File types to process
  "week_start_day": "monday",              // First day of week
  "currency": "AUD",                       // Currency symbol
  "field_aliases": {                       // Label customization
    "gross": "TOTAL",
    "net": "Net Pay",
    "tax": "TAX",
    // ... more aliases for your payslip labels
  }
}
```

## Troubleshooting

**Q: "No payslip files found"**
- Check that payslips are in the `input/` folder
- Verify file extensions are `.pdf` or `.txt`

**Q: "Could not extract data"**
- Ensure PDF is text-based (not scanned/image)
- Try opening PDF in text editor to verify content is readable
- Check `config.json` field aliases match your payslip labels

**Q: File says "locked" after running**
- Occurs when Excel file is open when tracker runs
- Automatic backup created with timestamp
- Close Excel file and run tracker again

## Privacy & Security

- **Input/Output folders are ignored**: `input/` and `output/` are in `.gitignore` - payslips won't be accidentally uploaded to GitHub
- **Local processing only**: All parsing happens on your computer; no data sent anywhere
- **Automatic backups**: Timestamped backups preserved in `output/backups/`

## Requirements

- Python 3.9+
- pandas (data processing)
- openpyxl (Excel file creation)
- PyPDF2 (PDF text extraction)
- python-dateutil (date parsing)

All dependencies listed in `requirements.txt`


