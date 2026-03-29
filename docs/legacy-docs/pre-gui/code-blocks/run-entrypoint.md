# run - Main Orchestration Function

**File:** `src/payslip_tracker.py`

## What It Is

`run()` is the entry point that ties every component together. When `payslip_tracker.py` is executed directly (via the batch file or command line), Python calls this function. It:

1. Resolves the project root and loads config.
2. Scans the `input/` directory for supported file types.
3. Extracts text from each file and parses it into a `PayslipRecord`.
4. Runs schema validation on every record.
5. Builds a sorted pandas DataFrame from all records.
6. Fills N/A for pay sections that are absent in a given payslip.
7. Detects missing weeks.
8. Writes a formatted Excel workbook (with a timestamped fallback name if the file is locked).
9. Writes a CSV export.
10. Prints a run summary to the console.

## Code Block

```python
from pathlib import Path
from dataclasses import asdict
from datetime import datetime as dt
import pandas as pd

def _write_excel(xlsx_path: Path, df: pd.DataFrame, missing_weeks: list[str]) -> None:
    """Write the main payslips sheet and the missing_weeks sheet, then apply formatting."""
    with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
        rename_for_excel(df).to_excel(writer, index=False, sheet_name="payslips")
        pd.DataFrame({"missing_week_start": missing_weeks}).to_excel(
            writer, index=False, sheet_name="missing_weeks", header=["Week Start"]
        )
    format_excel_output(xlsx_path)


def run() -> None:
    project_root = Path(__file__).resolve().parents[1]
    config = load_config(project_root)

    input_dir  = project_root / config.get("input_dir", "input")
    output_dir = project_root / config.get("output_dir", "output")
    output_dir.mkdir(parents=True, exist_ok=True)
    input_dir.mkdir(parents=True, exist_ok=True)

    supported = {ext.lower() for ext in config.get("supported_extensions", [".pdf", ".txt"])}
    files = [f for f in input_dir.iterdir() if f.is_file() and f.suffix.lower() in supported]

    if not files:
        print(f"No payslip files found in: {input_dir}")
        print("Add PDF/TXT payslips to input/ and re-run.")
        return

    records: list[PayslipRecord] = []
    for file_path in sorted(files):
        text   = read_text_from_file(file_path)
        record = parse_payslip(file_path, text, config)
        record = append_validation_notes(record)
        records.append(record)

    df = pd.DataFrame([asdict(r) for r in records])
    df = df.sort_values(
        by=["week_start", "pay_date", "file_name"], na_position="last"
    ).reset_index(drop=True)

    # Fill pay fields with N/A when not applicable
    ph_cols  = ["public_holiday_hours", "public_holiday_rate", "public_holiday_pay_this", "public_holiday_pay_ytd"]
    wk_cols  = ["weekend_hours", "weekend_rate", "weekend_pay_this", "weekend_pay_ytd"]
    ord_cols = ["ordinary_hours", "ordinary_rate", "ordinary_pay_this", "ordinary_pay_ytd"]
    df[ph_cols + wk_cols + ord_cols] = df[ph_cols + wk_cols + ord_cols].fillna("N/A")

    missing_weeks = find_missing_weeks(df)

    xlsx_path = output_dir / config.get("output_filename", "payslips.xlsx")
    csv_path  = output_dir / "payslips.csv"

    # Write Excel - fall back to timestamped name if the file is locked
    try:
        _write_excel(xlsx_path, df, missing_weeks)
    except PermissionError:
        backup_name = f"payslips_{dt.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        xlsx_path = output_dir / backup_name
        _write_excel(xlsx_path, df, missing_weeks)
        print(f"(Note: Main file was locked, saved as: {backup_name})")

    df.to_csv(csv_path, index=False)

    print(f"Processed {len(df)} payslip file(s)")
    print(f"Spreadsheet: {xlsx_path}")
    print(f"CSV: {csv_path}")

    if missing_weeks:
        print("Missing weekly payslips detected:")
        for w in missing_weeks:
            print(f"  - {w}")
    else:
        print("No missing weekly payslips detected in the observed range.")


if __name__ == "__main__":
    run()
```

## How to Re-Implement

1. Use `Path(__file__).resolve().parents[1]` to locate the project root relative to the script, making the entry point portable.
2. Use `.mkdir(parents=True, exist_ok=True)` for both `input/` and `output/` so first-time runs create the directories automatically.
3. Catch `PermissionError` when writing the Excel file so a locked spreadsheet does not crash the whole run - write a timestamped backup instead.
4. Keep the N/A fill step before `find_missing_weeks` so null checks in that function are unaffected.
5. Separate the `_write_excel` helper to avoid duplicating the pandas/openpyxl write logic in both the try and except branches.

### Running

```powershell
# Windows - double-click or:
python src\payslip_tracker.py

# macOS / Linux
python src/payslip_tracker.py
```
