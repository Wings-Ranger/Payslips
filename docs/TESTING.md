# Testing Guide

All tests live in the `tests/` directory and use [pytest](https://docs.pytest.org).

## Quick Start

```powershell
# Install dependencies (first time only)
pip install -r docs/requirements.txt
pip install pytest

# Run all tests from the project root
python -m pytest tests/ -v
```

## Test Files

| File | What it covers |
|---|---|
| `tests/test_parser.py` | `parse_payslip()`, `append_validation_notes()` |
| `tests/test_sheets.py` | `rename_for_excel()`, `find_missing_weeks()`, `add_pay_validation_columns()` |

## Test Descriptions

### test_parser.py

| Test | Description |
|---|---|
| `test_parse_scanned_text_sets_skip_note` | A PDF with fewer than 50 characters of extracted text is treated as a scanned image and gets a `SKIPPED` note. |
| `test_parse_missing_payment_date_adds_note` | When no `Payment Date:` line is found, the record's `notes` field contains `"Could not determine pay date"`. |
| `test_schema_validation_flags_missing_required_fields` | A record missing `net_this_pay` gets `SCHEMA_INVALID` appended to its notes by `append_validation_notes()`. |
| `test_total_hours_sums_all_hour_buckets` | `total_hours_this_pay` equals the sum of ordinary, weekend, and public holiday hours. |

### test_sheets.py

| Test | Description |
|---|---|
| `test_rename_for_excel_uses_human_headers` | `rename_for_excel()` maps snake_case column names to the human-readable labels defined in `EXCEL_HEADERS`. |
| `test_find_missing_weeks_detects_gap` | A two-row DataFrame with a one-week gap produces a list containing the missing ISO date string. |
| `test_find_missing_weeks_handles_empty_or_missing_column` | Returns an empty list for an empty DataFrame or a DataFrame with no `week_start` column. |
| `test_add_pay_validation_columns_pass_case` | All check columns are `PASS` when hours × rate equals recorded pay and net = gross − deductions. |
| `test_add_pay_validation_columns_fail_case` | `ordinary_check`, `net_check`, and `overall_pay_check` are `FAIL` when the figures do not reconcile. |

## Conventions

- Each test file adds `src/` to `sys.path` so imports resolve without installing the package.
- Tests pass plain `Path` objects and small literal text strings directly to parser functions — no fixture files are needed.
- The config fixture `_config()` returns `{"week_start_day": "monday"}`, which is the minimal config needed by the parser.
- There are no external dependencies beyond the packages listed in `docs/requirements.txt` and `pytest`.

## Coverage Areas Not Yet Tested

The following areas currently have no automated tests:

- `load_config()` — file-not-found and malformed JSON paths
- `read_text_from_file()` — actual PDF reading (requires a fixture PDF)
- `format_excel_output()` — openpyxl formatting (requires writing a real `.xlsx` file)
- `run()` — end-to-end integration (requires `input/` fixture files)
