# parse_payslip

**File:** `src/payslip_tracker.py`

## What It Is

`parse_payslip` is the core parsing engine. Given a file path, the extracted text string, and the config dict, it returns a fully-populated `PayslipRecord`. It uses a mix of single-line regex patterns and stateful line-by-line section scanning to pull structured data from free-form payslip text.

## Parsing Strategy Overview

| Stage | Technique | Target fields |
|-------|-----------|---------------|
| Scanned-PDF guard | Text length check (`< 50` chars) | All — returns early with a SKIPPED note |
| Employee name | First non-empty line | `employee` |
| Pay period | Regex on normalised text | `pay_period` |
| Payment date | Regex on normalised text + `dateutil` | `pay_date`, `week_start` |
| Salary & Wages section | Stateful line scanner (start: `"salary & wages"`, end: `"tax"`) | `ordinary_*`, `weekend_*`, `public_holiday_*`, `gross_*` |
| Tax section | Stateful line scanner (start: `"tax"`, end: `"payment details"`) | `payg_*`, `tax_*` |
| Net Pay | Regex on normalised text | `net_this_pay` |
| Total hours | Arithmetic sum of hour fields | `total_hours_this_pay` |

## Code Block

```python
import re
from pathlib import Path
from datetime import datetime
from dateutil import parser as date_parser

def parse_payslip(file_path: Path, text: str, config: dict) -> PayslipRecord:
    # Guard: scanned PDF with no extractable text
    if len(text.strip()) < 50:
        return PayslipRecord(
            file_name=file_path.name,
            employee=None,
            pay_date=None,
            pay_period=None,
            week_start=None,
            notes="SKIPPED: Scanned PDF, needs OCR.",
        )

    # Employee name = first non-empty line
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    employee_raw = lines[0] if lines else None

    # Normalise for single-line regex patterns
    text_normalized = text.replace("\n", " ")

    # Pay period
    pay_period = None
    m = re.search(
        r"pay period:\s*(\d{1,2}/\d{1,2}/\d{4})\s*-\s*(\d{1,2}/\d{1,2}/\d{4})",
        text_normalized, re.IGNORECASE,
    )
    if m:
        pay_period = f"{m.group(1)} - {m.group(2)}"

    # Payment date
    pay_date = None
    m = re.search(r"payment date:\s*(\d{1,2}/\d{1,2}/\d{4})", text_normalized, re.IGNORECASE)
    if m:
        try:
            pay_date = date_parser.parse(m.group(1), dayfirst=True).date().isoformat()
        except Exception:
            pass

    # ---- Salary & Wages section ----
    ordinary_hours = ordinary_rate = ordinary_pay_this = ordinary_pay_ytd = None
    weekend_hours = weekend_rate = weekend_pay_this = weekend_pay_ytd = None
    public_holiday_hours = public_holiday_rate = public_holiday_pay_this = public_holiday_pay_ytd = None
    gross_this_pay = gross_ytd = None

    in_salary_section = False
    for line in text.splitlines():
        line_lower = line.lower()
        if "salary & wages" in line_lower:
            in_salary_section = True
            continue
        if in_salary_section and ("tax" in line_lower or line_lower.startswith("tax")):
            in_salary_section = False
        if in_salary_section:
            parts = re.findall(r"[\d.]+", line)
            if "ordinary hours" in line_lower and len(parts) >= 4:
                ordinary_hours, ordinary_rate, ordinary_pay_this, ordinary_pay_ytd = map(float, parts[:4])
            elif "weekends" in line_lower and ("sat" in line_lower or "sun" in line_lower) and len(parts) >= 4:
                weekend_hours, weekend_rate, weekend_pay_this, weekend_pay_ytd = map(float, parts[:4])
            elif "public" in line_lower and "holiday" in line_lower and len(parts) >= 4:
                public_holiday_hours, public_holiday_rate, public_holiday_pay_this, public_holiday_pay_ytd = map(float, parts[:4])
            elif line_lower.strip().startswith("total") and len(parts) >= 2:
                gross_this_pay, gross_ytd = float(parts[0]), float(parts[1])

    # ---- Tax section ----
    payg_this_pay = payg_ytd = tax_this_pay = tax_ytd = None

    in_tax_section = False
    for line in text.splitlines():
        line_lower = line.lower()
        if line_lower.startswith("tax"):
            in_tax_section = True
            continue
        if in_tax_section and "payment details" in line_lower:
            in_tax_section = False
        if in_tax_section:
            parts = re.findall(r"[\d.]+", line)
            if "payg" in line_lower and len(parts) >= 2:
                payg_this_pay, payg_ytd = float(parts[0]), float(parts[1])
            elif "tax" in line_lower and "payg" not in line_lower and line_lower.strip() != "tax" and len(parts) >= 2:
                tax_this_pay, tax_ytd = float(parts[0]), float(parts[1])
            elif line_lower.strip().startswith("total") and len(parts) >= 2 and tax_this_pay is None:
                tax_this_pay, tax_ytd = float(parts[0]), float(parts[1])

    # Net Pay
    net_this_pay = None
    m = re.search(r"net pay:\s*\$?([\d.]+)", text_normalized, re.IGNORECASE)
    if m:
        try:
            net_this_pay = float(m.group(1))
        except ValueError:
            pass

    # Total hours
    total_hours_this_pay = sum(filter(None, [ordinary_hours, weekend_hours, public_holiday_hours])) or None

    # Week start
    week_start = None
    if pay_date:
        try:
            week_start = get_week_start(
                datetime.fromisoformat(pay_date),
                config.get("week_start_day", "monday"),
            ).date().isoformat()
        except Exception:
            pass

    notes = []
    if pay_date is None:
        notes.append("Could not determine pay date")

    return PayslipRecord(
        file_name=file_path.name,
        employee=employee_raw,
        pay_date=pay_date,
        pay_period=pay_period,
        week_start=week_start,
        ordinary_hours=ordinary_hours,
        ordinary_rate=ordinary_rate,
        ordinary_pay_this=ordinary_pay_this,
        ordinary_pay_ytd=ordinary_pay_ytd,
        weekend_hours=weekend_hours,
        weekend_rate=weekend_rate,
        weekend_pay_this=weekend_pay_this,
        weekend_pay_ytd=weekend_pay_ytd,
        public_holiday_hours=public_holiday_hours,
        public_holiday_rate=public_holiday_rate,
        public_holiday_pay_this=public_holiday_pay_this,
        public_holiday_pay_ytd=public_holiday_pay_ytd,
        gross_this_pay=gross_this_pay,
        gross_ytd=gross_ytd,
        tax_this_pay=tax_this_pay,
        tax_ytd=tax_ytd,
        payg_this_pay=payg_this_pay,
        payg_ytd=payg_ytd,
        net_this_pay=net_this_pay,
        net_ytd=None,  # not present in current payslip format
        total_hours_this_pay=total_hours_this_pay,
        notes="; ".join(notes),
    )
```

## How to Re-Implement

1. **Guard clause first** — reject files with fewer than 50 extractable characters as scanned images.
2. **Employee name** — assume the first non-empty line of the document is the employee's name.
3. **Regex on normalised text** — collapse newlines into spaces before running regex patterns that may span line-wrapped text.
4. **Section scanning** — use a boolean flag (`in_salary_section`, `in_tax_section`) toggled by sentinel words. Iterate lines and parse specific sub-patterns within each section.
5. **Number extraction** — `re.findall(r"[\d.]+", line)` extracts all numeric tokens from a line regardless of currency symbols or commas; map them positionally to the expected fields.
6. **Error safety** — wrap every `float()` conversion in a `try/except` so a malformed line never crashes the parser; leave the field as `None`.
7. **Week start** — derive from `pay_date` using [`get_week_start`](get-week-start.md).

## Expected Input Format

```
Jane Citizen
Pay Period: 01/03/2026 - 07/03/2026
Payment Date: 07/03/2026
Salary & Wages
Ordinary Hours 37.5000 16.7100 626.63 18453.56
Weekends Sat/Sun 10.0000 21.8000 218.00 4352.33
Public Holiday 7.5000 30.0000 225.00 900.00
TOTAL 1069.63 23705.89
Tax
PAYG 0.00 264.00
TOTAL 0.00 264.00
Net Pay: 1069.63
```
