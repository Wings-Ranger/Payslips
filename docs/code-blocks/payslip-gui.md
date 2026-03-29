# PayslipTrackerApp — Desktop GUI

**File:** `src/payslip_gui.py`

## What It Is

`PayslipTrackerApp` is the Tkinter desktop interface for the Payslip Tracker. It provides a non-terminal workflow for selecting folders, starting processing, viewing progress, reading errors, and opening the generated spreadsheet.

## Main Features

- input folder picker
- output folder picker
- recent-folder history dropdowns
- Run button
- progress/status log
- summary panel with processed/skipped/missing-week counts
- error panel
- Open Spreadsheet button

## Design Notes

- Processing runs on a background thread so the UI stays responsive.
- A queue bridges worker-thread updates back to the Tkinter main loop.
- Recent folders are stored in `.payslip_tracker_ui.json` at the project root.
- The GUI depends on `process_payslips()` rather than duplicating business logic.

## Re-Implementation Guidance

1. Keep all long-running work off the Tkinter main thread.
2. Use a queue plus periodic polling for thread-safe UI updates.
3. Persist lightweight UI state separately from processing config.
4. Treat the GUI as a thin wrapper over the reusable processing service.
