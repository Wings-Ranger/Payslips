# add_pay_validation_columns

**File:** `src/payslip_tracker.py`

## What It Is

`add_pay_validation_columns` takes the main payslip DataFrame and appends six extra columns that cross-check whether the parsed numeric figures are internally consistent. Each check compares expected values (calculated from hours × rate, or from summing pay components) against the figures actually extracted from the payslip text.

| Column | Check performed |
|--------|-----------------|
| `ordinary_check` | `ordinary_hours × ordinary_rate ≈ ordinary_pay_this` |
| `weekend_check` | `weekend_hours × weekend_rate ≈ weekend_pay_this` |
| `public_holiday_check` | `public_holiday_hours × public_holiday_rate ≈ public_holiday_pay_this` |
| `gross_check` | `ordinary_pay_this + weekend_pay_this + public_holiday_pay_this ≈ gross_this_pay` |
| `net_check` | `gross_this_pay − tax_this_pay − payg_this_pay ≈ net_this_pay` |
| `overall_pay_check` | `PASS` only when every other check is `PASS` |

Values are `"PASS"`, `"FAIL"`, or `"N/A"` when one or more inputs needed for the check are absent or non-numeric.

A tolerance of `$0.02` is applied to every comparison to absorb rounding differences in the payslip source document.

## Code Block

```python
import pandas as pd

def add_pay_validation_columns(df: pd.DataFrame) -> pd.DataFrame:
    _TOL = 0.02

    def _numeric(val) -> float | None:
        try:
            v = float(val)
            return v if v == v else None  # reject NaN
        except (TypeError, ValueError):
            return None

    def _hours_rate_check(hours_val, rate_val, pay_val) -> str:
        h, r, p = _numeric(hours_val), _numeric(rate_val), _numeric(pay_val)
        if h is None or r is None or p is None:
            return "N/A"
        return "PASS" if abs(h * r - p) <= _TOL else "FAIL"

    out = df.copy()

    out["ordinary_check"] = [
        _hours_rate_check(r["ordinary_hours"], r["ordinary_rate"], r["ordinary_pay_this"])
        for _, r in df.iterrows()
    ]
    out["weekend_check"] = [
        _hours_rate_check(r["weekend_hours"], r["weekend_rate"], r["weekend_pay_this"])
        for _, r in df.iterrows()
    ]
    out["public_holiday_check"] = [
        _hours_rate_check(r["public_holiday_hours"], r["public_holiday_rate"], r["public_holiday_pay_this"])
        for _, r in df.iterrows()
    ]

    gross_checks = []
    net_checks = []
    for _, r in df.iterrows():
        ord_pay = _numeric(r["ordinary_pay_this"]) or 0.0
        wk_pay = _numeric(r["weekend_pay_this"]) or 0.0
        ph_pay = _numeric(r["public_holiday_pay_this"]) or 0.0
        gross = _numeric(r["gross_this_pay"])
        if gross is None:
            gross_checks.append("N/A")
        else:
            gross_checks.append("PASS" if abs(ord_pay + wk_pay + ph_pay - gross) <= _TOL else "FAIL")

        tax = _numeric(r["tax_this_pay"]) or 0.0
        payg = _numeric(r["payg_this_pay"]) or 0.0
        net = _numeric(r["net_this_pay"])
        if gross is None or net is None:
            net_checks.append("N/A")
        else:
            net_checks.append("PASS" if abs(gross - tax - payg - net) <= _TOL else "FAIL")

    out["gross_check"] = gross_checks
    out["net_check"] = net_checks

    check_cols = ["ordinary_check", "weekend_check", "public_holiday_check", "gross_check", "net_check"]
    overall = []
    for _, r in out.iterrows():
        values = [r[c] for c in check_cols]
        if any(v == "FAIL" for v in values):
            overall.append("FAIL")
        elif all(v == "PASS" for v in values):
            overall.append("PASS")
        else:
            overall.append("N/A")
    out["overall_pay_check"] = overall

    return out
```

## How to Re-Implement

1. Copy the DataFrame before adding columns (`df.copy()`) so the original is not mutated.
2. Use a small helper (`_numeric`) that converts any value — including `"N/A"` strings — to `float | None`, so the function works on the DataFrame both before and after the N/A fill step.
3. Apply a `_TOL` rounding tolerance (e.g. `$0.02`) to account for truncation differences in payslip source documents.
4. Treat `None` inputs as `"N/A"` rather than `"FAIL"` to distinguish between a parsing failure and a genuine mismatch.

### Usage

```python
df = pd.DataFrame([asdict(r) for r in records])
# … sort, N/A-fill …
df = add_pay_validation_columns(df)

# Rows with any failed check
failures = df[df["overall_pay_check"] == "FAIL"]
```
