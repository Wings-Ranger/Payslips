# Technique: Config-Driven Paths and Runtime Behavior

## Purpose

Keep environment-specific choices and evolving parser aliases outside application logic.

## Where Used

- `load_config()`, `process_payslips()`, and `get_project_root()` in `src/payslip_tracker.py`
- `src/config.json`
- packaged PyInstaller builds that bundle config into the app

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
3. Check both source-tree and packaged-app config locations.
4. Add new config keys in docs and tests together.

## Common Pitfalls

- Relative-path assumptions when script is launched from a different working directory.
- Adding config keys that are never consumed in code.
- Silent fallback to defaults that hides configuration mistakes.
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
