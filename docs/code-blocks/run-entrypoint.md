# run / process_payslips — Main Orchestration Layer

**File:** `src/payslip_tracker.py`

## What It Is

`process_payslips()` is the reusable orchestration layer for the application. It is called by the GUI, tests, and the console wrapper `run()`. The smaller `run()` function now prints a console summary around the result returned by `process_payslips()`.

The processing pipeline:

1. Resolves the project root and loads config.
2. Resolves input/output folders from config or explicit overrides.
3. Scans the chosen input directory for supported file types.
4. Extracts text from each file and parses it into a `PayslipRecord`.
5. Runs schema validation on every record.
6. Builds a sorted pandas DataFrame from all records.
7. Fills N/A for pay sections that are absent in a given payslip.
8. Detects missing weeks.
9. Writes a formatted Excel workbook (with a timestamped fallback name if the file is locked).
10. Writes a CSV export.
11. Returns a `ProcessResult` for the caller.

The console wrapper:

1. Calls `process_payslips()`.
2. Prints a console summary.
3. Handles the no-files-found case with a user-friendly message.

## Code Block

```python
from pathlib import Path
from typing import Callable

@dataclass
class ProcessResult:
    input_dir: Path
    output_dir: Path
    files_found: int
    processed_count: int
    skipped_count: int
    schema_invalid_count: int
    missing_weeks: list[str]
    xlsx_path: Path
    csv_path: Path
    opened_spreadsheet: bool = False


def process_payslips(
    *,
    project_root: Path | None = None,
    input_dir: Path | str | None = None,
    output_dir: Path | str | None = None,
    open_spreadsheet: bool = False,
    status_callback: Callable[[str], None] | None = None,
) -> ProcessResult:
    ...

def run() -> None:
    try:
        result = process_payslips()
    except FileNotFoundError as exc:
        print(exc)
        print("Add PDF/TXT payslips to input/ and re-run.")
        return

    print(f"Processed {result.processed_count} payslip file(s)")
    print(f"Spreadsheet: {result.xlsx_path}")
    print(f"CSV: {result.csv_path}")


if __name__ == "__main__":
    run()
```

## How to Re-Implement

1. Keep a reusable service function separate from console/UI code.
2. Accept directory overrides so a GUI or tests can control runtime paths without editing config.
3. Use a result object to return counts, output paths, and missing weeks cleanly.
4. Keep status reporting callback-based so the GUI can show progress without coupling the processing code to Tkinter.
5. Preserve a tiny `run()` wrapper for command-line compatibility.

### Running

```powershell
# Windows GUI
python src\payslip_gui.py

# Windows console wrapper
python src\payslip_tracker.py

# macOS / Linux
python src/payslip_tracker.py
```
