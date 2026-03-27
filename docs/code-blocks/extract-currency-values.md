# extract_currency_values

**File:** `src/payslip_tracker.py`

## What It Is

`extract_currency_values` is a small utility that extracts every numeric token from a single line of payslip text and returns them as a list of `float` values. It strips currency symbols, commas, and any other non-numeric characters, making it safe to call on raw payslip lines such as:

```
TOTAL $234.32 $12,235.23
Ordinary Hours 7.5000 $16.7100 $125.32 $7,337.90
```

It is used by the debug scripts (`debug_parse.py`, `debug_parse2.py`) to inspect what values the section-scanning parser would extract from a given line.

## Code Block

```python
import re

def extract_currency_values(line: str) -> list[float]:
    """Extract all numeric values from a text line as floats."""
    return [float(x) for x in re.findall(r"[\d.]+", line)]
```

## How to Re-Implement

1. `re.findall(r"[\d.]+", line)` matches every sequence of digit and dot characters. This intentionally ignores `$`, `,`, and spaces so it works regardless of currency formatting.
2. Map each match to `float()` immediately — payslip values are always representable as floats at the precision used.
3. The order of the returned values mirrors the order they appear in the line, which is the positional mapping used by `parse_payslip()` (hours, rate, this-pay, YTD).

### Usage

```python
line = "Ordinary Hours 7.5000 $16.7100 $125.32 $7,337.90"
values = extract_currency_values(line)
# values == [7.5, 16.71, 125.32, 7337.9]

hours, rate, pay_this, pay_ytd = values[:4]
```
