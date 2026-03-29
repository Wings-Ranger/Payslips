# Technique: Section Scanning Plus Regex Extraction

## Purpose

Extract structured fields from semi-structured payslip text without requiring a full parser framework.

## Where Used

- `parse_payslip()` in `src/payslip_tracker.py`

## Core Pattern

1. Split text into lines.
2. Track current section using sentinel phrases (`salary & wages`, `tax`).
3. Apply targeted regex extraction only within relevant sections.
4. Use specific line predicates for each data row (`ordinary hours`, `weekends`, `public holiday`, `total`).

## Why This Approach Fits

- Payslip formats are mostly predictable but not strict enough for a fixed-column parser.
- Section boundaries reduce false positives from global regex matching.
- Keeping extraction line-scoped makes troubleshooting easier during format drift.

## Practical Guidance

- Prefer lowercased line checks (`line_lower`) for robust matching.
- Use normalized single-line text (`text_normalized`) for fields that span line breaks.
- Parse date-like tokens separately from monetary values.
- Keep extraction tolerant: assign values only when enough numeric tokens are found.

## Risks and Mitigations

- Risk: Vendor wording changes break section start/end detection.
  - Mitigation: add aliases in config and tests for new formats.
- Risk: Numeric token regex can over-capture malformed values.
  - Mitigation: wrap float conversion in try/except and preserve parse notes.
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
