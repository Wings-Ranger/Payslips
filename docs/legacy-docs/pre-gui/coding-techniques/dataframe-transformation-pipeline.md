# Technique: DataFrame Transformation Pipeline

## Purpose

Convert parsed records into a consistent tabular form for sorting, enrichment, and multi-format export.

## Where Used

- `run()` in `src/payslip_tracker.py`

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

This is a legacy document. For beginner-friendly foundations, start with [../../../building-blocks/README.md](../../../building-blocks/README.md).
Then return here only if you specifically need the pre-GUI historical implementation details.

## When This Is Not The Best Fit

- This file documents an older architecture and may not match the current app flow.
- Prefer current docs in docs/code-blocks and docs/coding-techniques for active implementation work.
- Use this as reference context, not as a copy-paste template.
