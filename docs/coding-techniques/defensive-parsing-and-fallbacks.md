# Technique: Defensive Parsing and Fallback Notes

## Purpose

Preserve pipeline stability when input quality is inconsistent (scanned PDFs, missing values, malformed lines).

## Where Used

- `parse_payslip()` in `src/payslip_tracker.py`
- `append_validation_notes()` in `src/payslip_tracker.py`

## Defensive Patterns Used

- Early skip for likely scanned PDFs (`text.strip()` length threshold).
- Try/except around float/date conversion to avoid hard failures.
- `None` defaults for uncertain fields instead of incorrect fabricated values.
- Post-parse note aggregation for missing critical fields.
- Schema validation notes appended rather than replacing existing notes.

## Why This Matters

- The workflow processes batches of files; one bad file should not stop all outputs.
- Auditable notes make data quality visible in exported sheets.
- Parsing errors become testable behavior instead of silent corruption.

## Practical Guidance

1. Fail soft in parsing, fail loud in notes.
2. Keep notes machine-searchable (`SCHEMA_INVALID`, `SKIPPED`).
3. Distinguish parse-time anomalies from business-rule validation failures.
4. Add a focused unit test each time a new fallback path is introduced.
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
