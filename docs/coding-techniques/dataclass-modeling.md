# Technique: Typed Record Modeling with Dataclasses

## Purpose

Use a dataclass as the canonical in-memory model for one parsed payslip record. This keeps parsing logic, validation logic, and export logic aligned around one field set.

## Where Used

- `PayslipRecord` in `src/payslip_tracker.py`
- `asdict(record)` conversion before DataFrame creation

## Why It Works Well Here

- Provides explicit field names and optional types for partially parsed data.
- Makes schema validation straightforward because fields are centralized.
- Reduces accidental key mismatches that are common in ad-hoc dictionaries.

## Implementation Notes

1. Keep fields grouped by domain (identity, hours/rates, totals, notes).
2. Use `Optional[...]` for parser outputs that may be absent.
3. Keep `notes` as a freeform field for diagnostic and validation annotations.
4. Convert to dictionaries only at the export boundary (`asdict`).

## Guardrails

- Add new fields to `PayslipRecord` first, then update:
  - parser assignment
  - header mapping (`EXCEL_HEADERS`)
  - tests that assert expected columns and checks
- Avoid storing derived values if they can be computed reliably from base fields unless needed downstream.
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
