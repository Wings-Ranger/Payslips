# Technique: Config-Driven Paths and Runtime Behavior

## Purpose

Keep environment-specific choices and evolving parser aliases outside application logic.

## Where Used

- `load_config()` and `run()` in `src/payslip_tracker.py`
- `src/config.json`

## Configurable Concerns

- Input/output directories.
- Output file naming.
- Supported file extensions.
- Week start day used in missing-week calculations.
- Field aliases for future parser flexibility.

## Design Benefits

- Deploys across machines without code edits.
- Makes defaults explicit and versionable.
- Reduces hardcoded strings and brittle paths.

## Implementation Guidance

1. Resolve all runtime paths from project root with `Path`.
2. Keep safe defaults in code for missing keys.
3. Validate config file existence early and fail with clear error text.
4. Add new config keys in docs and tests together.

## Common Pitfalls

- Relative-path assumptions when script is launched from a different working directory.
- Adding config keys that are never consumed in code.
- Silent fallback to defaults that hides configuration mistakes.
## Beginner Ramp-Up

This is a legacy document. For beginner-friendly foundations, start with [../../../building-blocks/README.md](../../../building-blocks/README.md).
Then return here only if you specifically need the pre-GUI historical implementation details.

## When This Is Not The Best Fit

- This file documents an older architecture and may not match the current app flow.
- Prefer current docs in docs/code-blocks and docs/coding-techniques for active implementation work.
- Use this as reference context, not as a copy-paste template.
