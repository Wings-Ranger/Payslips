# Code Blocks — Index

This directory contains one Markdown file per unique code block in the Payslips repository. Each file explains what the block does and how to re-implement it from scratch.

For technique-level guidance (patterns that span multiple functions/files), see [../coding-techniques/README.md](../coding-techniques/README.md).

## Core Application (`src/payslip_tracker.py`)

| File | Code Block | Description |
|------|------------|-------------|
| [payslip-record-dataclass.md](payslip-record-dataclass.md) | `PayslipRecord` | Typed dataclass holding all fields extracted from one payslip |
| [load-config.md](load-config.md) | `load_config()` | Load `src/config.json` relative to the project root |
| [read-text-from-file.md](read-text-from-file.md) | `read_text_from_file()` | Extract plain text from PDF or TXT payslip files |
| [extract-currency-values.md](extract-currency-values.md) | `extract_currency_values()` | Extract all numeric tokens from a payslip text line as floats |
| [get-week-start.md](get-week-start.md) | `get_week_start()` | Calculate the most recent occurrence of a chosen weekday |
| [parse-payslip.md](parse-payslip.md) | `parse_payslip()` | Core parser — extract all fields from payslip text via regex and section scanning |
| [find-missing-weeks.md](find-missing-weeks.md) | `find_missing_weeks()` | Detect gaps in weekly payslip coverage |
| [format-excel-output.md](format-excel-output.md) | `format_excel_output()` | Apply colour coding, borders, and number formats to the Excel workbook |
| [excel-headers-and-rename.md](excel-headers-and-rename.md) | `EXCEL_HEADERS` + `rename_for_excel()` | Map snake_case field names to human-readable Excel headers |
| [pay-validation-columns.md](pay-validation-columns.md) | `add_pay_validation_columns()` | Append cross-check columns verifying internal pay figure consistency |
| [schema-validation.md](schema-validation.md) | `REQUIRED_SCHEMA_FIELDS` + `validate_record_schema()` + `append_validation_notes()` | Flag records with missing required fields |
| [run-entrypoint.md](run-entrypoint.md) | `run()` + `_write_excel()` | Main orchestration function — scan, parse, validate, export |

## Configuration

| File | Code Block | Description |
|------|------------|-------------|
| [config-json.md](config-json.md) | `src/config.json` | Runtime configuration schema and all available keys |

## Windows Entry Point

| File | Code Block | Description |
|------|------------|-------------|
| [process-payslips-bat.md](process-payslips-bat.md) | `Process Payslips.bat` | Double-click Windows launcher for end users |

## Developer / Debug Scripts (`scripts/`)

| File | Code Block | Description |
|------|------------|-------------|
| [script-check-headers.md](script-check-headers.md) | `check_headers.py` | Print the first 10 Excel column headers for a quick sanity check |
| [script-debug-parse.md](script-debug-parse.md) | `debug_parse.py` + `debug_parse2.py` | Step through the section-scanning parser to diagnose mismatches |
| [script-debug-sheets.md](script-debug-sheets.md) | `debug_sheets.py` | Inspect CSV data types and test summary-sheet functions |
| [script-show-all-headers.md](script-show-all-headers.md) | `show_all_headers.py` | Print all Excel column headers plus sample data rows |
| [script-show-lines.md](script-show-lines.md) | `show_lines.py` | Print the first 25 raw text lines of a payslip file |
| [script-update-headers.md](script-update-headers.md) | `update_headers.py` | One-time migration script that added human-readable Excel headers |
| [script-view-sheets.md](script-view-sheets.md) | `view_sheets.py` | Dump all rows from named Excel sheets to the console |
