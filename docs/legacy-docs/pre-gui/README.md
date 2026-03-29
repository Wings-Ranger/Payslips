# Payslip Tracker - Technical Documentation

Automatically parse payslip PDFs/TXT files, detect missing weeks, and generate formatted Excel reports.

## Project Structure

```
Payslips/
  Process Payslips.bat   # Entry point - double-click to run
  input/                 # Drop payslip files here
  output/                # Generated reports appear here
  src/
    config.json          # Runtime configuration
    payslip_tracker.py   # Main application
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

## Architecture

### Data Flow

1. `run()` scans `input/` for supported files (`.pdf`, `.txt`)
2. `read_text_from_file()` extracts raw text (PyPDF2 for PDFs)
3. `parse_payslip()` extracts structured fields via regex into `PayslipRecord`
4. `append_validation_notes()` flags records missing required schema fields
5. DataFrame is built, sorted by `week_start`, and N/A-filled for empty pay sections
6. `add_pay_validation_columns()` appends cross-check columns verifying internal pay consistency
7. `find_missing_weeks()` detects gaps in weekly payslip coverage
8. Excel output with `rename_for_excel()` human-readable headers + `format_excel_output()` styling
9. CSV export for external tooling

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

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r docs/requirements.txt
python src/payslip_tracker.py
```

## Dependencies

- Python 3.9+
- pandas, openpyxl, PyPDF2, python-dateutil

## Privacy

- `input/` and `output/` are in `.gitignore`
- All processing is local - no data leaves your machine
## Beginner Ramp-Up

This is a legacy document. For beginner-friendly foundations, start with [../../building-blocks/README.md](../../building-blocks/README.md).
Then return here only if you specifically need the pre-GUI historical implementation details.

## When This Is Not The Best Fit

- This file documents an older architecture and may not match the current app flow.
- Prefer current docs in docs/code-blocks and docs/coding-techniques for active implementation work.
- Use this as reference context, not as a copy-paste template.
