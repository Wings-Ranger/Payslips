@echo off
cd /d %~dp0

where pyw >nul 2>nul
if %errorlevel% equ 0 (
  start "" pyw src\payslip_gui.py
  exit /b 0
)

start "Payslip Tracker" py src\payslip_gui.py