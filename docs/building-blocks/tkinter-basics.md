# Building Block: Tkinter Basics

## Goal

Understand enough Tkinter to safely maintain the desktop app.

## Beginner Concepts

- Main thread: owns UI updates.
- Worker thread: runs long processing tasks.
- Queue/polling: sends messages from worker to UI thread.
- Styles: central place for colors/fonts.

## Architecture Pattern

Use a thin UI layer and a separate processing service.

- UI responsibilities: collect input, show status, render errors.
- Service responsibilities: parse/process/export.
- Bridge: callback or queue messages from worker to UI.

This keeps GUI changes from breaking processing logic.

## Beginner Implementation Steps

1. Build a minimal window with one button and one status label.
2. Move long-running work into a worker thread.
3. Send progress messages to a queue.
4. Poll queue from the main thread and update UI.
5. Add theme values and apply them in one styling function.

## Threading Safety Rules

- Do not update Tk widgets directly from worker threads.
- Use `after(...)` polling to process queue messages on the main loop.
- Disable run/start controls while processing to avoid duplicate worker jobs.
- Re-enable controls in a guaranteed completion path, including errors.

## UI Reliability Checks

1. Window remains responsive during long runs.
2. Progress messages appear in order.
3. Errors are visible and not swallowed.
4. Final summary renders even when some files are skipped.

## When Tkinter Is Not Ideal

- If you need web deployment, use a web framework instead.
- If you need very advanced desktop widgets, consider Qt or similar.

## Maintainability Tip

Keep all theme keys centralized so missing keys fall back to defaults instead of breaking widget creation.
