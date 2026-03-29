# load_config

**File:** `src/payslip_tracker.py`

## What It Is

`load_config` loads the JSON configuration file and merges it over built-in defaults. It supports both source-tree and packaged-app layouts by checking multiple candidate locations before raising `FileNotFoundError`.

## Code Block

```python
import json
import sys
from pathlib import Path


DEFAULT_CONFIG = {
    "week_start_day": "monday",
    "currency_symbol": "AUD",
    "input_dir": "input",
    "output_dir": "output",
    "output_filename": "payslips.xlsx",
    "supported_extensions": [".pdf", ".txt"],
}


def _candidate_config_paths(project_root: Path) -> list[Path]:
    candidates = [project_root / "src" / "config.json", project_root / "config.json"]
    bundle_root = getattr(sys, "_MEIPASS", None)
    if bundle_root:
        bundle_path = Path(bundle_root)
        candidates.extend([bundle_path / "src" / "config.json", bundle_path / "config.json"])
    return candidates

def load_config(project_root: Path) -> dict:
    for config_path in _candidate_config_paths(project_root):
        if config_path.exists():
            with config_path.open("r", encoding="utf-8") as f:
                loaded = json.load(f)
            return {**DEFAULT_CONFIG, **loaded}
    raise FileNotFoundError("Missing config file")
```

## How to Re-Implement

1. Accept the project root as a `Path` argument so the function is portable and testable regardless of the working directory.
2. Check source and packaged-app paths rather than assuming only one layout.
3. Merge the loaded file over in-code defaults so missing keys do not crash the app.
4. Open with `encoding="utf-8"` to handle any Unicode characters in the config.

### Usage

```python
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]
config = load_config(project_root)

input_dir  = project_root / config.get("input_dir", "input")
output_dir = project_root / config.get("output_dir", "output")
week_start = config.get("week_start_day", "monday")
```

### Config file location

The function first checks `<project_root>/src/config.json`, then `<project_root>/config.json`, and also packaged-app locations when running under PyInstaller.
See [`config-json.md`](config-json.md) for the full schema and all available keys.
## Beginner Ramp-Up

If this feels advanced, read these first:

- [../building-blocks/implementation-basics.md](../building-blocks/implementation-basics.md)
- [../building-blocks/configuration-and-paths.md](../building-blocks/configuration-and-paths.md)
- [../building-blocks/python-data-models.md](../building-blocks/python-data-models.md)
- [../building-blocks/regex-basics.md](../building-blocks/regex-basics.md)
- [../building-blocks/dataframe-basics.md](../building-blocks/dataframe-basics.md)
- [../building-blocks/testing-basics.md](../building-blocks/testing-basics.md)
- [../building-blocks/tkinter-basics.md](../building-blocks/tkinter-basics.md)

Follow this order: building block -> this file's implementation steps -> tests.

## When This Is Not The Best Fit

- If your requirements are much simpler, prefer a smaller implementation.
- If your input format differs heavily, adapt the pattern rather than copying it exactly.
- If this is a one-time script, consider readability-first code before framework-style structure.
