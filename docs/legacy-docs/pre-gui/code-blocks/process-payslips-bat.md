# Process Payslips.bat - Windows Entry Point

**File:** `Process Payslips.bat`

## What It Is

`Process Payslips.bat` is the Windows batch-file entry point for end users who do not want to open a terminal. Double-clicking the file:

1. Changes the working directory to the folder that contains the `.bat` file (using `%~dp0`).
2. Sets a friendly title, colour scheme, and window size so the terminal looks approachable to non-technical users.
3. Shows a clear header and step-by-step description before any work starts.
4. Runs the Python tracker with `py src\payslip_tracker.py`.
5. If the script exits with a non-zero error code, switches to a red colour scheme, prints a plain-English error message, and pauses so the user can read it before the window closes.
6. If the output file `output\payslips.xlsx` exists, it opens it in the default spreadsheet application.
7. Prints a completion message and closes the window automatically.

## Terminal Preview

| Normal run | On error |
|---|---|
| ![Payslip Tracker terminal - normal run (blue screen) and error run (red screen)](https://github.com/user-attachments/assets/ba721c5d-e1a1-42bd-9761-48dcadd08870) | *(same image - error screen shown in lower half)* |

The upper half shows the blue welcome screen with a step-by-step description; the lower half shows how the screen switches to red when something goes wrong.

## Code Block

```bat
@echo off
cd /d %~dp0

title Payslip Tracker
color 1F
mode con cols=70 lines=25

echo.
echo  ============================================================
echo    Payslip Tracker
echo  ============================================================
echo.
echo    This tool reads your payslip files and builds a tidy
echo    spreadsheet for you automatically.
echo.
echo    Steps it will follow:
echo      1. Read payslip files from the input folder
echo      2. Build your spreadsheet
echo      3. Open the finished spreadsheet when done
echo.
echo  ------------------------------------------------------------
echo.
echo  Starting... please wait.
echo.

py src\payslip_tracker.py

if %errorlevel% neq 0 (
  echo.
  color 4F
  echo  ============================================================
  echo    Something went wrong
  echo  ============================================================
  echo.
  echo    Please check:
  echo      - Your payslip files are in the input folder
  echo      - Files are saved as .pdf or .txt
  echo.
  echo    If the problem keeps happening, ask your IT support team
  echo    and show them this window.
  echo.
  echo  ------------------------------------------------------------
  pause
  exit /b %errorlevel%
)

if exist output\payslips.xlsx (
  echo  Opening your spreadsheet...
  start "" output\payslips.xlsx
)

echo.
echo  ============================================================
echo    All done!
echo  ============================================================
echo.
echo    Your output files are saved in the output folder.
echo.
echo  ------------------------------------------------------------
```

## Key Techniques

| Technique | Purpose |
|-----------|---------|
| `@echo off` | Suppress command echoing for a clean console output. |
| `cd /d %~dp0` | Change to the script's own directory, so relative paths like `src\` and `output\` always resolve correctly regardless of where the user double-clicks from. |
| `title Payslip Tracker` | Sets the window title bar text so the window is clearly labelled instead of showing the raw script path. |
| `color 1F` | Sets the terminal to a blue background (`1`) with bright white text (`F`) for a clean, professional look. The format is `XY` where `X` = background and `Y` = foreground, using standard Windows console colour codes. |
| `color 4F` | Switches to a red background (`4`) with bright white text (`F`) in the error path so the user immediately sees something needs attention. |
| `mode con cols=70 lines=25` | Sets the console window to a comfortable fixed size so it does not open as a narrow default window. |
| Bordered header block | `echo` lines with `=` and `-` borders create a simple, readable layout without requiring any external tools. |
| `py` instead of `python` | Uses the Windows Python Launcher (`py.exe`), which is available on Windows 10/11 and respects `#!` shebangs and version pins. |
| `%errorlevel%` check | Propagates the Python exit code so the user knows whether the run succeeded or failed. |
| `start "" output\payslips.xlsx` | Opens the file with its associated application (Excel or LibreOffice Calc) without blocking the batch script. The empty `""` is a required placeholder for the window title. |
| `pause` (error path only) | Keeps the terminal window open on failure so the user can read the error message before it closes. On a successful run the window closes automatically. |

## How to Re-Implement

Create a `.bat` file at the project root with the pattern above. Adjust the Python command if needed:

```bat
@echo off
cd /d %~dp0

title My Script
color 1F
mode con cols=70 lines=25

echo.
echo  ============================================================
echo    My Script
echo  ============================================================
echo.
echo  Starting... please wait.
echo.

py src\my_script.py

if %errorlevel% neq 0 (
  color 4F
  echo  Something went wrong. See above for details.
  pause
  exit /b %errorlevel%
)

echo  Done.
```

To open a different output file:

```bat
if exist output\report.xlsx (
  start "" output\report.xlsx
)
```

### Windows console colour codes

| Code | Colour |
|------|--------|
| 0 | Black |
| 1 | Dark Blue |
| 2 | Dark Green |
| 3 | Dark Cyan |
| 4 | Dark Red |
| 5 | Dark Magenta |
| 6 | Dark Yellow (Brown) |
| 7 | Light Grey |
| 8 | Dark Grey |
| 9 | Blue |
| A | Green |
| B | Cyan |
| C | Red |
| D | Magenta |
| E | Yellow |
| F | Bright White |
