# PayslipRecord Dataclass

**File:** `src/payslip_tracker.py`

## What It Is

`PayslipRecord` is a typed data container that holds every field extracted from a single payslip file. It uses Python's `@dataclass` decorator and `Optional` type hints to make it clear which fields are guaranteed to be present and which may be absent when parsing fails or a section does not exist in the payslip.

The dataclass is converted to a plain dict via `dataclasses.asdict()` before being loaded into a pandas DataFrame for reporting.

## Code Block

```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class PayslipRecord:
    file_name: str
    employee: Optional[str]
    pay_date: Optional[str]
    pay_period: Optional[str]
    week_start: Optional[str]
    # Ordinary hours
    ordinary_hours: Optional[float] = None
    ordinary_rate: Optional[float] = None
    ordinary_pay_this: Optional[float] = None
    ordinary_pay_ytd: Optional[float] = None
    # Weekend hours
    weekend_hours: Optional[float] = None
    weekend_rate: Optional[float] = None
    weekend_pay_this: Optional[float] = None
    weekend_pay_ytd: Optional[float] = None
    # Public holiday hours
    public_holiday_hours: Optional[float] = None
    public_holiday_rate: Optional[float] = None
    public_holiday_pay_this: Optional[float] = None
    public_holiday_pay_ytd: Optional[float] = None
    # Totals
    gross_this_pay: Optional[float] = None
    gross_ytd: Optional[float] = None
    tax_this_pay: Optional[float] = None
    tax_ytd: Optional[float] = None
    payg_this_pay: Optional[float] = None
    payg_ytd: Optional[float] = None
    net_this_pay: Optional[float] = None
    net_ytd: Optional[float] = None
    total_hours_this_pay: Optional[float] = None
    notes: str = ""
```

## Field Groups

| Group | Fields |
|-------|--------|
| Identity | `file_name`, `employee`, `pay_date`, `pay_period`, `week_start` |
| Ordinary hours | `ordinary_hours`, `ordinary_rate`, `ordinary_pay_this`, `ordinary_pay_ytd` |
| Weekend hours | `weekend_hours`, `weekend_rate`, `weekend_pay_this`, `weekend_pay_ytd` |
| Public holiday | `public_holiday_hours`, `public_holiday_rate`, `public_holiday_pay_this`, `public_holiday_pay_ytd` |
| Totals | `gross_this_pay`, `gross_ytd`, `tax_this_pay`, `tax_ytd`, `payg_this_pay`, `payg_ytd`, `net_this_pay`, `net_ytd`, `total_hours_this_pay` |
| Metadata | `notes` |

## How to Re-Implement

1. Add `from dataclasses import dataclass, asdict` and `from typing import Optional` to your imports.
2. Annotate the class with `@dataclass`.
3. List fields with positional (required) ones first — `file_name`, `employee`, `pay_date`, `pay_period`, `week_start` — then optional numeric fields with `= None` defaults, and finally `notes: str = ""`.
4. Use `asdict(record)` when you need a plain dict (e.g. to build a pandas DataFrame row).

```python
from dataclasses import dataclass, asdict

record = PayslipRecord(
    file_name="pay_2026-03-07.txt",
    employee="Jane Citizen",
    pay_date="2026-03-07",
    pay_period="2026-03-01 - 2026-03-07",
    week_start="2026-03-02",
    ordinary_hours=37.5,
    net_this_pay=1234.56,
)

row = asdict(record)  # convert to dict for DataFrame
```
