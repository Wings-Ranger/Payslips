# process_payslips / ProcessResult

**File:** `src/payslip_tracker.py`

## What It Is

`process_payslips()` is the reusable application service that powers the GUI, tests, and console wrapper. It performs the full parse/export pipeline and returns a `ProcessResult` object containing summary counts, output paths, and missing-week information.

## Why It Exists

The older `run()` implementation mixed orchestration with console printing. Splitting the real work into `process_payslips()` makes the code usable from:

- the Tkinter GUI
- unit tests
- the command-line wrapper
- future packaged or scripted entry points

## Core Contract

- Accept optional `project_root`, `input_dir`, and `output_dir` overrides.
- Accept an optional `status_callback` for progress updates.
- Raise `FileNotFoundError` when no supported files are found.
- Return a `ProcessResult` on success.

## Result Shape

`ProcessResult` reports:

- input and output directories used
- total files found
- processed file count
- skipped file count
- schema-invalid count
- missing week list
- Excel and CSV output paths

## Re-Implementation Guidance

1. Keep this function free of GUI-specific code.
2. Push progress updates through a callback rather than direct printing.
3. Return structured results rather than expecting callers to scrape console text.
4. Let small wrappers decide whether to print, render UI, or open files.
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
