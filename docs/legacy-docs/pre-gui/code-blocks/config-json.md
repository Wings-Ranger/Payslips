# config.json - Configuration Schema

**File:** `src/config.json`

## What It Is

`config.json` is the runtime configuration file for the Payslip Tracker. It is loaded once at startup by `load_config()` and passed through to the parsing and output functions.

## Current Content

```json
{
  "week_start_day": "monday",
  "currency_symbol": "AUD",
  "input_dir": "input",
  "output_dir": "output",
  "output_filename": "payslips.xlsx",
  "supported_extensions": [".pdf", ".txt"],
  "field_aliases": {
    "gross":       ["gross", "gross pay", "total gross", "total earnings"],
    "net":         ["net", "net pay", "take home"],
    "tax":         ["tax", "paye", "income tax", "payg"],
    "ni":          ["ni", "national insurance", "super", "superannuation"],
    "hours":       ["hours", "hours worked", "total hours", "ordinary hours", "weekends"],
    "pay_date":    ["payment date", "date paid", "pay date"],
    "pay_period":  ["pay period"],
    "employee":    ["employee", "name", "employee name"]
  }
}
```

## Key Reference

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `week_start_day` | string | `"monday"` | First day of the pay week used by `get_week_start()`. Accepts any lowercase weekday name. |
| `currency_symbol` | string | `"AUD"` | Currency label (informational — not used in calculations). |
| `input_dir` | string | `"input"` | Directory scanned for payslip files, relative to the project root. |
| `output_dir` | string | `"output"` | Directory where Excel and CSV reports are written, relative to the project root. |
| `output_filename` | string | `"payslips.xlsx"` | Name of the primary Excel output file. |
| `supported_extensions` | array of strings | `[".pdf", ".txt"]` | File extensions that will be processed. Extensions are matched case-insensitively. |
| `field_aliases` | object | (see above) | Maps canonical field names to alternative label strings found in payslip text. Not yet consumed by the current parser but reserved for future alias-driven parsing. |

## How to Re-Implement

Create `src/config.json` in your project with the keys above. To load it:

```python
import json
from pathlib import Path

config_path = Path(__file__).resolve().parents[1] / "src" / "config.json"
with config_path.open("r", encoding="utf-8") as f:
    config = json.load(f)

week_start  = config.get("week_start_day", "monday")
input_dir   = Path(config.get("input_dir", "input"))
output_dir  = Path(config.get("output_dir", "output"))
extensions  = {ext.lower() for ext in config.get("supported_extensions", [".pdf", ".txt"])}
```

### Changing the week start day

If your organisation's pay week starts on Thursday:

```json
{
  "week_start_day": "thursday"
}
```

### Adding a new supported file type

```json
{
  "supported_extensions": [".pdf", ".txt", ".docx"]
}
```

Remember to also add a corresponding branch in `read_text_from_file()`.
