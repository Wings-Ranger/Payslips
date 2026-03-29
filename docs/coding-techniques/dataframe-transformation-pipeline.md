# Technique: DataFrame Transformation Pipeline

## Purpose

Convert parsed records into a consistent tabular form for sorting, enrichment, and multi-format export.

## Where Used

- `process_payslips()` in `src/payslip_tracker.py`

## Pipeline Stages

1. Convert parsed records with `asdict` into a DataFrame.
2. Sort rows by temporal keys (`week_start`, `pay_date`) and stable tie-breaker (`file_name`).
3. Fill missing pay buckets with explicit `"N/A"` markers for readability.
4. Compute derived views and checks before output.
5. Export to Excel and CSV.

## Why This Pattern Works

- Keeps parsing concerns separate from tabular output concerns.
- Makes ordering deterministic for diff-friendly outputs.
- Enables layered enrichment (validation columns, renamed headers) without mutating parser logic.

## Guidance for Future Changes

- Keep all column additions in one stage to avoid hidden side effects.
- Be explicit when mixing numeric and string placeholders (`"N/A"`).
- Add tests when sorting keys or fill behavior changes.
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
