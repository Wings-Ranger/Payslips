@echo off
cd /d %~dp0\..
echo Building Payslip Tracker .exe ...
pyinstaller --noconfirm "build\Payslip Tracker.spec"
if %errorlevel% neq 0 (
    echo Build failed.
    pause
    exit /b %errorlevel%
)
echo.
echo Build complete. The exe is in: dist\Payslip Tracker\
echo Config is bundled into the app build.
echo Share this folder along with input/ and output/ if needed.
pause
