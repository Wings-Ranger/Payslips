# add_pay_validation_columns — Pay Accuracy Cross-Check

**File:** `src/payslip_tracker.py`

## What It Is

`add_pay_validation_columns()` takes a DataFrame of parsed payslip records and appends five `PASS`/`FAIL` columns that cross-check the numeric pay figures against each other. It lets you confirm that hours × rate matches the recorded pay, that component pays add up to gross, and that gross minus deductions equals net — all without leaving the spreadsheet.

| Column added | Check performed |
|---|---|
| `ordinary_check` | `ordinary_hours × ordinary_rate ≈ ordinary_pay_this` |
| `weekend_check` | `weekend_hours × weekend_rate ≈ weekend_pay_this` |
| `gross_check` | `ordinary_pay_this + weekend_pay_this + public_holiday_pay_this ≈ gross_this_pay` |
| `net_check` | `gross_this_pay − tax_this_pay − payg_this_pay ≈ net_this_pay` |
| `overall_pay_check` | `PASS` only when all four checks above are `PASS` |

A tolerance of **$0.02** is applied to each comparison to absorb standard rounding differences.

## Code Block

```python
_PAY_CHECK_TOLERANCE = 0.02  # maximum cent difference treated as a rounding pass


def add_pay_validation_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Add PASS/FAIL columns that cross-check parsed pay figures for accuracy."""

    def _pass_fail(diff: pd.Series) -> pd.Series:
        """Convert a Series of absolute differences to PASS/FAIL strings."""
        return (diff.abs() <= _PAY_CHECK_TOLERANCE).map({True: "PASS", False: "FAIL"})

    df = df.copy()

    # Coerce to numeric so vectorised arithmetic works even when columns contain
    # "N/A" strings from the earlier N/A fill step.
    num = {
        col: pd.to_numeric(df[col], errors="coerce")
        for col in [
            "ordinary_hours", "ordinary_rate", "ordinary_pay_this",
            "weekend_hours", "weekend_rate", "weekend_pay_this",
            "public_holiday_pay_this",
            "gross_this_pay", "tax_this_pay", "payg_this_pay", "net_this_pay",
        ]
    }

    df["ordinary_check"] = _pass_fail(
        num["ordinary_hours"] * num["ordinary_rate"] - num["ordinary_pay_this"]
    )
    df["weekend_check"] = _pass_fail(
        num["weekend_hours"] * num["weekend_rate"] - num["weekend_pay_this"]
    )
    df["gross_check"] = _pass_fail(
        num["ordinary_pay_this"] + num["weekend_pay_this"] + num["public_holiday_pay_this"]
        - num["gross_this_pay"]
    )
    df["net_check"] = _pass_fail(
        num["gross_this_pay"] - num["tax_this_pay"] - num["payg_this_pay"] - num["net_this_pay"]
    )
    check_cols = ["ordinary_check", "weekend_check", "gross_check", "net_check"]
    df["overall_pay_check"] = (
        (df[check_cols] == "PASS").all(axis=1).map({True: "PASS", False: "FAIL"})
    )

    return df
```

## How to Re-Implement

1. Keep a module-level tolerance constant (`_PAY_CHECK_TOLERANCE = 0.02`) so the rounding threshold is easy to adjust without touching the function body.
2. Use `pd.to_numeric(df[col], errors="coerce")` on every input column before doing arithmetic. This handles `"N/A"` strings that the earlier N/A fill step may have left in the DataFrame — they coerce silently to `NaN`, which propagates through the arithmetic and maps to `"FAIL"` when the diff cannot be computed.
3. The inner `_pass_fail()` helper works on whole Series at once, so all rows are evaluated in a single vectorised operation rather than a Python loop.
4. Derive `overall_pay_check` last, after the four individual columns exist, so it can aggregate them with `.all(axis=1)`.
5. Return `df.copy()` rather than mutating the caller's DataFrame.

### Usage

```python
df = pd.DataFrame([asdict(r) for r in records])
df = add_pay_validation_columns(df)

# Flag rows where something doesn't add up
problem_rows = df[df["overall_pay_check"] == "FAIL"]
print(problem_rows[["file_name", "ordinary_check", "weekend_check", "gross_check", "net_check"]])
```

### Adjusting the tolerance

The default tolerance is **$0.02**. If your payroll system rounds to the nearest 5 cents you could raise it:

```python
_PAY_CHECK_TOLERANCE = 0.05
```
