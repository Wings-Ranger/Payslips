# Technique: Tolerance-Based Business Rule Validation

## Purpose

Detect numeric inconsistencies across related pay fields while accounting for rounding behavior.

## Where Used

- `add_pay_validation_columns()` in `src/payslip_tracker.py`
- Assertions in `tests/test_sheets.py`

## Validation Style

- Compute expected values from base components (for example, `hours * rate`).
- Compare expected vs observed using a small tolerance (`0.02`).
- Produce categorical outcomes per check: `PASS`, `FAIL`, `N/A`.
- Aggregate individual checks into an `overall_pay_check` status.

## Why Categorical Output

- Easy to scan in Excel exports.
- Useful for downstream filtering and audit workflows.
- Avoids exposing raw floating-point drift to end users.

## Implementation Guidance

1. Normalize numeric inputs through a single helper (`_numeric`).
2. Treat missing values as `N/A` where the check cannot be computed.
3. Keep tolerance in one constant so policy changes are simple.
4. Include both pass and fail unit tests for each validation group.
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
