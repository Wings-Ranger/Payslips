# Technique: Presentation-Layer Formatting for Excel Outputs

## Purpose

Separate data correctness from human-readable spreadsheet presentation.

## Where Used

- `format_excel_output()` in `src/payslip_tracker.py`

## Formatting Techniques Applied

- Section-based color coding by pay category.
- Header styling with contrast and centered labels.
- Explicit column widths by semantic role.
- Number formats by type (currency, numeric hours/rates, dates).
- Borders and frozen panes for large-sheet navigation.
- Missing-weeks sheet styling that highlights blank cells.

## Design Principle

Export clean data first, then apply presentation rules in a dedicated formatting step.

## Benefits

- Easier debugging when parse values are wrong versus when display looks wrong.
- Safer future changes to report appearance.
- Consistent user experience across reruns.

## Guidance

1. Keep format constants centralized in one function.
2. Use column-letter maps intentionally; update them when schema shifts.
3. Preserve raw values and rely on Excel number formats rather than stringifying currency.
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
