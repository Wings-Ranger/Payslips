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
