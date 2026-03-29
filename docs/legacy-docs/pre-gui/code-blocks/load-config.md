# load_config

**File:** `src/payslip_tracker.py`

## What It Is

`load_config` loads the JSON configuration file (`src/config.json`) relative to the project root and returns it as a Python dict. It raises a descriptive `FileNotFoundError` if the config file is missing, preventing silent failures at startup.

## Code Block

```python
import json
from pathlib import Path

def load_config(project_root: Path) -> dict:
    config_path = project_root / "src" / "config.json"
    if not config_path.exists():
        raise FileNotFoundError(f"Missing config file: {config_path}")
    with config_path.open("r", encoding="utf-8") as f:
        return json.load(f)
```

## How to Re-Implement

1. Accept the project root as a `Path` argument so the function is portable and testable regardless of the working directory.
2. Build the config path relative to that root.
3. Check `.exists()` before opening to give a clear error message.
4. Open with `encoding="utf-8"` to handle any Unicode characters in the config.

### Usage

```python
from pathlib import Path

project_root = Path(__file__).resolve().parents[1]  # two levels up from src/
config = load_config(project_root)

input_dir  = project_root / config.get("input_dir", "input")
output_dir = project_root / config.get("output_dir", "output")
week_start = config.get("week_start_day", "monday")
```

### Config file location

The function expects the config at `<project_root>/src/config.json`.
See [`config-json.md`](config-json.md) for the full schema and all available keys.
