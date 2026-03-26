@echo off
cd /d %~dp0
echo Building Payslip Tracker .exe ...
pyinstaller --noconfirm --clean --name "Payslip Tracker" --distpath dist --workpath build\pyinstaller --specpath build src\payslip_tracker.py
if %errorlevel% neq 0 (
    echo Build failed.
    pause
    exit /b %errorlevel%
)
echo.
echo Build complete. The exe is in: dist\Payslip Tracker\
echo Share this folder along with input/, output/, and src/config.json
pause
