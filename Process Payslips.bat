@echo off
cd /d %~dp0

if exist "portable\Payslip Tracker Portable\Payslip Tracker\Payslip Tracker.exe" (
  start "" "portable\Payslip Tracker Portable\Payslip Tracker\Payslip Tracker.exe"
  exit /b 0
)

if exist "dist\Payslip Tracker\Payslip Tracker.exe" (
  start "" "dist\Payslip Tracker\Payslip Tracker.exe"
  exit /b 0
)

where pyw >nul 2>nul
if %errorlevel% equ 0 (
  start "" pyw src\payslip_gui.py
  exit /b 0
)

start "Payslip Tracker" py src\payslip_gui.py