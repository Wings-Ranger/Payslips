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
