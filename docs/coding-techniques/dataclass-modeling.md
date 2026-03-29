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
