# Process Payslips.bat — Windows Entry Point

**File:** `Process Payslips.bat`

## What It Is

`Process Payslips.bat` is the Windows batch-file entry point for end users who do not want to open a terminal. Double-clicking the file:

1. Changes the working directory to the folder that contains the `.bat` file (using `%~dp0`).
2. Checks whether `pyw` is available.
3. Launches the desktop GUI with `pyw src\payslip_gui.py` when possible so no console window stays attached.
4. Falls back to `py src\payslip_gui.py` if `pyw` is unavailable.

## Current Code Block

## Code Block

```bat
@echo off
cd /d %~dp0

where pyw >nul 2>nul
if %errorlevel% equ 0 (
  start "" pyw src\payslip_gui.py
  exit /b 0
)

start "Payslip Tracker" py src\payslip_gui.py
```

## Key Techniques

| Technique | Purpose |
|-----------|---------|
| `@echo off` | Suppress command echoing for a clean launcher. |
| `cd /d %~dp0` | Change to the script's own directory, so relative paths like `src\` and `output\` always resolve correctly regardless of where the user double-clicks from. |
| `where pyw >nul 2>nul` | Detect whether the windowless Python launcher is available. |
| `pyw` first | Starts the GUI without attaching a visible console window. |
| `start` | Launches the GUI asynchronously so the batch file can exit immediately. |
| fallback to `py` | Preserves compatibility on systems that do not have `pyw` available. |

## How to Re-Implement

Create a `.bat` file at the project root with the pattern above. Adjust the Python command if needed:

```bat
@echo off
cd /d %~dp0

where pyw >nul 2>nul
if %errorlevel% equ 0 (
  start "" pyw src\my_gui.py
  exit /b 0
)

start "My App" py src\my_gui.py
```
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
