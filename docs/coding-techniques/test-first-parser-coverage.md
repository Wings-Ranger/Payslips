# Technique: Focused Unit Tests for Parser and Validation Logic

## Purpose

Validate behavior of parser edge cases and cross-field calculations using compact synthetic fixtures.

## Where Used

- `tests/test_parser.py`
- `tests/test_sheets.py`

## Testing Patterns

- Build minimal multiline text fixtures directly in tests.
- Assert behavior, not implementation details.
- Include both nominal and failure-path cases.
- Validate user-visible diagnostics in notes and check columns.

## Coverage Areas in This Repo

- Scanned text skip handling.
- Missing payment date annotations.
- Schema validation note injection.
- Total-hours rollups across pay buckets.
- Missing-week detection.
- PASS/FAIL outcomes for business-rule checks.

## Practical Guidance

1. Add one test per newly discovered real-world format variance.
2. Keep fixture text short but semantically representative.
3. When changing tolerance or formulas, update pass and fail tests together.
