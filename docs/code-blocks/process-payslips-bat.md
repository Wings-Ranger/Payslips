# Process Payslips.bat — Windows Entry Point

**File:** `Process Payslips.bat`

## What It Is

`Process Payslips.bat` is the Windows batch-file entry point for end users who do not want to open a terminal. Double-clicking the file:

1. Changes the working directory to the folder that contains the `.bat` file (using `%~dp0`).
2. Runs the Python tracker with `py src\payslip_tracker.py`.
3. If the script exits with a non-zero error code, it prints a user-friendly message and pauses so the user can read it before the window closes.
4. If the output file `output\payslips.xlsx` exists, it opens it in the default spreadsheet application.
5. Prints a completion message and pauses.

## Code Block

```bat
@echo off
cd /d %~dp0

echo Running Payslip Tracker...
py src\payslip_tracker.py

if %errorlevel% neq 0 (
  echo.
  echo The tracker hit an error.
  echo Please check that payslip files are in the input folder and try again.
  pause
  exit /b %errorlevel%
)

if exist output\payslips.xlsx (
  echo Opening spreadsheet...
  start "" output\payslips.xlsx
)

echo.
echo Done. Your output files are in the output folder.
pause
```

## Key Techniques

| Technique | Purpose |
|-----------|---------|
| `@echo off` | Suppress command echoing for a clean console output. |
| `cd /d %~dp0` | Change to the script's own directory, so relative paths like `src\` and `output\` always resolve correctly regardless of where the user double-clicks from. |
| `py` instead of `python` | Uses the Windows Python Launcher (`py.exe`), which is available on Windows 10/11 and respects `#!` shebangs and version pins. |
| `%errorlevel%` check | Propagates the Python exit code so the user knows whether the run succeeded or failed. |
| `start "" output\payslips.xlsx` | Opens the file with its associated application (Excel or LibreOffice Calc) without blocking the batch script. The empty `""` is a required placeholder for the window title. |
| Final `pause` | Keeps the terminal window open so the user can read the output before it closes. |

## How to Re-Implement

Create a `.bat` file at the project root with the pattern above. Adjust the Python command if needed:

```bat
@echo off
cd /d %~dp0
echo Running My Script...
py src\my_script.py
if %errorlevel% neq 0 (
  echo Script failed. See above for details.
  pause
  exit /b %errorlevel%
)
echo Done.
pause
```

To open a different output file:

```bat
if exist output\report.xlsx (
  start "" output\report.xlsx
)
```
