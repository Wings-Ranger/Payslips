# get_week_start

**File:** `src/payslip_tracker.py`

## What It Is

`get_week_start` calculates the date of the most-recent occurrence of a chosen weekday on or before a given `datetime`. It is used to normalise every payslip's pay date to the start of its reporting week, so that records can be grouped, sorted, and gap-checked consistently.

The `start_day` parameter defaults to `"monday"` and is driven by the `week_start_day` key in `config.json`.

## Code Block

```python
from datetime import datetime, timedelta

def get_week_start(dt: datetime, start_day: str = "monday") -> datetime:
    weekdays = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6,
    }
    target = weekdays.get(start_day.lower(), 0)
    offset = (dt.weekday() - target) % 7
    return dt - timedelta(days=offset)
```

## How It Works

`datetime.weekday()` returns 0 for Monday through 6 for Sunday.  
The modulo expression `(dt.weekday() - target) % 7` always produces a value in `[0, 6]` — the number of days to subtract to reach the previous (or same-day) occurrence of `target`. Subtracting that offset from `dt` gives the week-start date.

### Examples

| `dt` | `start_day` | Result |
|------|-------------|--------|
| Wednesday 2026-03-04 | `"monday"` | 2026-03-02 (Mon) |
| Wednesday 2026-03-04 | `"wednesday"` | 2026-03-04 (same day) |
| Monday 2026-03-02 | `"sunday"` | 2026-02-22 (previous Sun) |

## How to Re-Implement

1. Build a lookup dict mapping lowercase weekday names to Python's `weekday()` integers (Monday = 0).
2. Use `.get(start_day.lower(), 0)` so an unrecognised value safely falls back to Monday.
3. Compute the offset using the `% 7` trick to handle wrap-around correctly.
4. Return `dt - timedelta(days=offset)`.

### Usage

```python
from datetime import datetime

pay_date = datetime(2026, 3, 7)  # Saturday
week_start = get_week_start(pay_date, start_day="monday")
print(week_start.date())  # 2026-03-02
```
