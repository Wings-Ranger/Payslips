# PayslipTrackerApp — Desktop GUI

**File:** `src/payslip_gui.py`

## What It Is

`PayslipTrackerApp` is the Tkinter desktop interface for the Payslip Tracker. It provides a non-terminal workflow for selecting folders, starting processing, viewing progress, reading errors, and opening the generated spreadsheet.

## Main Features

- input folder picker
- output folder picker
- recent-folder history dropdowns
- beginner-editable theme file
- live theme reload button
- open-theme-file shortcut
- Run button
- progress/status log
- summary panel with processed/skipped/missing-week counts
- error panel
- Open Spreadsheet button

## Design Notes

- Processing runs on a background thread so the UI stays responsive.
- A queue bridges worker-thread updates back to the Tkinter main loop.
- Recent folders are stored in `.payslip_tracker_ui.json` at the project root.
- Visual styling is loaded from `ui_theme.json` so beginners can restyle the app without changing Python code.
- The GUI depends on `process_payslips()` rather than duplicating business logic.

## Re-Implementation Guidance

1. Keep all long-running work off the Tkinter main thread.
2. Use a queue plus periodic polling for thread-safe UI updates.
3. Persist lightweight UI state separately from processing config.
4. Keep appearance settings in a simple JSON theme file rather than hardcoding them into widget creation.
5. Treat the GUI as a thin wrapper over the reusable processing service.
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
