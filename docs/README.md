# Payslip Tracker - Technical Documentation

Automatically parse payslip PDFs/TXT files, detect missing weeks, and generate formatted Excel reports.

## Project Structure

```
Payslips/
  Process Payslips.bat   # Entry point - double-click to run
  ui_theme.json          # Beginner-editable GUI theme
  input/                 # Drop payslip files here
  output/                # Generated reports appear here
  src/
    config.json          # Runtime configuration
    payslip_tracker.py   # Main application
    payslip_gui.py       # Desktop GUI launcher
  scripts/               # Dev/debug utilities
  tests/                 # Unit tests
  docs/
    README.md            # This file
    coding-techniques/   # Technique-oriented implementation notes
    code-blocks/         # Function-by-function code block notes
    requirements.txt     # Python dependencies
```

## Documentation Sets

- [coding-techniques/README.md](coding-techniques/README.md): one file per reusable coding technique used across the repository.
- [code-blocks/README.md](code-blocks/README.md): one file per concrete code block or function.
- [theme-guide/README.md](theme-guide/README.md): field-by-field guide to `ui_theme.json` with links to the relevant GUI code lines.
- [legacy-docs/README.md](legacy-docs/README.md): archived pre-GUI documentation kept for reference only.

## Architecture

### Data Flow

1. `Process Payslips.bat` launches the desktop GUI on Windows.
2. `payslip_gui.py` loads `ui_theme.json`, remembers recent locations, and starts processing in a background thread.
3. `process_payslips()` scans the chosen input folder for supported files (`.pdf`, `.txt`).
4. `read_text_from_file()` extracts raw text (PyPDF2 for PDFs).
5. `parse_payslip()` extracts structured fields via regex into `PayslipRecord`.
6. `append_validation_notes()` flags records missing required schema fields.
7. DataFrame is built, sorted by `week_start`, and N/A-filled for empty pay sections.
8. `find_missing_weeks()` detects gaps in weekly payslip coverage.
9. Excel output with `rename_for_excel()` human-readable headers + `format_excel_output()` styling.
10. CSV export is written for external tooling.
11. GUI shows progress, summary counts, and errors, then lets the user open the spreadsheet.
12. Users can edit `ui_theme.json` and reload the visual theme without restarting the app.

### PayslipRecord Fields (27 fields)

| Category | Fields |
|----------|--------|
| Identity | `file_name`, `employee`, `pay_date`, `pay_period`, `week_start` |
| Ordinary | `ordinary_hours`, `ordinary_rate`, `ordinary_pay_this`, `ordinary_pay_ytd` |
| Weekend | `weekend_hours`, `weekend_rate`, `weekend_pay_this`, `weekend_pay_ytd` |
| Public Holiday | `public_holiday_hours`, `public_holiday_rate`, `public_holiday_pay_this`, `public_holiday_pay_ytd` |
| Totals | `gross_this_pay`, `gross_ytd`, `tax_this_pay`, `tax_ytd`, `payg_this_pay`, `payg_ytd`, `net_this_pay`, `net_ytd`, `total_hours_this_pay` |
| Metadata | `notes` |

### Parsing Strategy

- **Salary & Wages section**: Line-by-line scan between "salary & wages" and "tax" markers
  - Matches "ordinary hours", "weekends sat/sun", "public holiday" lines
  - Extracts 4 numeric fields per line: hours, rate, this-pay, YTD
  - "TOTAL" line captures gross this-pay and YTD
- **Tax section**: Between "tax" header and "payment details"
  - Matches "payg" and other tax lines
  - "TOTAL" fallback if no specific tax line found
- **Net Pay**: Regex on normalized (single-line) text
- **Scanned PDFs**: Detected when extracted text < 50 chars, flagged as SKIPPED

### Excel Formatting

- Color-coded sections: ordinary (blue), weekend (yellow), public holiday (green), gross (orange), tax (red)
- Currency columns formatted as `$#,##0.00`
- Notes column: wrapped text, left-aligned
- Missing weeks sheet: black-filled empty cells, frozen header
- Pay sections filled with "N/A" when not applicable to a payslip

### Schema Validation

Required fields: `file_name`, `employee`, `pay_date`, `week_start`, `net_this_pay`

Records missing required fields get `SCHEMA_INVALID` appended to notes.

## Configuration

`src/config.json`:

| Key | Default | Description |
|-----|---------|-------------|
| `input_dir` | `"input"` | Payslip source directory |
| `output_dir` | `"output"` | Report output directory |
| `output_filename` | `"payslips.xlsx"` | Excel filename |
| `supported_extensions` | `[".pdf", ".txt"]` | File types to process |
| `week_start_day` | `"monday"` | First day of pay week |
| `currency_symbol` | `"AUD"` | Currency label (informational — not used in calculations). |
| `field_aliases` | (see `src/config.json`) | Maps canonical field names to alternative label strings found in payslip text. Reserved for future alias-driven parsing. |

`load_config()` looks for config in packaged and source layouts, then merges the file over built-in defaults.

`ui_theme.json`:

- Controls the GUI window title, fonts, colors, spacing, and button/section labels.
- Is intended to be beginner-editable without changing Python code.
- Can be reloaded live from the GUI.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r docs/requirements.txt
python src/payslip_gui.py
```

For a packaged Windows build:

```powershell
scripts\build_exe.bat
```

## Dependencies

- Python 3.9+
- pandas, openpyxl, PyPDF2, python-dateutil

## Privacy

- `input/` and `output/` are in `.gitignore`
- All processing is local - no data leaves your machine
