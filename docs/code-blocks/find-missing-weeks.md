# find_missing_weeks

**File:** `src/payslip_tracker.py`

## What It Is

`find_missing_weeks` inspects a DataFrame for gaps in weekly payslip coverage. It collects the unique `week_start` values, builds the expected set of weekly dates from the earliest to the latest observed week, and returns any dates that are missing from the data.

The result is written to the `missing_weeks` sheet in the Excel output and printed to the console at the end of a run.

## Code Block

```python
import pandas as pd
from datetime import datetime, timedelta

def find_missing_weeks(df: pd.DataFrame) -> list[str]:
    if df.empty or "week_start" not in df.columns:
        return []

    valid = df["week_start"].dropna().unique().tolist()
    if not valid:
        return []

    weeks = sorted(datetime.fromisoformat(x).date() for x in valid)
    start = weeks[0]
    end   = weeks[-1]

    observed = set(weeks)
    missing  = []

    current = start
    while current <= end:
        if current not in observed:
            missing.append(current.isoformat())
        current += timedelta(days=7)

    return missing
```

## How It Works

1. Filter out `None` / NaN values from the `week_start` column.
2. Parse the ISO-format date strings into `date` objects and sort them.
3. Walk from the first to the last observed week in 7-day steps.
4. Any step that is not in the observed set is a missing week.

## Edge Cases

- Returns `[]` when the DataFrame is empty or has no `week_start` column.
- Returns `[]` when all `week_start` values are `None`/NaN.
- Returns `[]` when there is only one week (no gaps possible).

## How to Re-Implement

```python
from datetime import datetime, timedelta
import pandas as pd

df = pd.read_csv("output/payslips.csv")
missing = find_missing_weeks(df)

if missing:
    print("Missing weeks:")
    for w in missing:
        print(f"  {w}")
else:
    print("No gaps detected.")
```

### Writing to Excel

```python
pd.DataFrame({"missing_week_start": missing}).to_excel(
    writer, index=False, sheet_name="missing_weeks", header=["Week Start"]
)
```
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
