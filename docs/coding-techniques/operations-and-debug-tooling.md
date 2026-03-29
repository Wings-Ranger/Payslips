# Technique: Small-Purpose Operational and Debug Scripts

## Purpose

Use lightweight one-task scripts to inspect outputs, debug parser behavior, and support one-time migration actions.

## Where Used

- `scripts/check_headers.py`
- `scripts/debug_parse.py`
- `scripts/debug_parse2.py`
- `scripts/debug_sheets.py`
- `scripts/show_all_headers.py`
- `scripts/show_lines.py`
- `scripts/update_headers.py`
- `scripts/view_sheets.py`

## Script Design Pattern

- Single responsibility per script.
- Direct, readable console output.
- Minimal dependencies beyond project libs.
- Safe read-only diagnostics for most scripts.

## Why This Is Effective

- Speeds up troubleshooting without cluttering production code.
- Allows quick experiments with parser assumptions.
- Provides operational checks that non-developers can run.

## Guidance

1. Keep debug scripts explicit, not generic frameworks.
2. Prefix temporary scripts with intent and remove stale ones over time.
3. Add short docs entries for any script expected to be reused.
