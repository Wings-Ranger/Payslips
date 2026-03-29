@echo off
cd /d %~dp0\..

set "PY_CMD="
where py >nul 2>nul
if not errorlevel 1 set "PY_CMD=py"

if not defined PY_CMD (
    where python >nul 2>nul
    if not errorlevel 1 set "PY_CMD=python"
)

if not defined PY_CMD (
    echo Could not find Python launcher ^(`py` or `python`^).
    pause
    exit /b 1
)

%PY_CMD% -m PyInstaller --version >nul 2>nul
if errorlevel 1 (
    echo PyInstaller not found. Installing it now...
    %PY_CMD% -m pip install --upgrade pip
    if errorlevel 1 (
        echo Failed to upgrade pip.
        pause
        exit /b %errorlevel%
    )

    %PY_CMD% -m pip install pyinstaller
    if errorlevel 1 (
        echo Failed to install PyInstaller.
        pause
        exit /b %errorlevel%
    )
)

echo Building Payslip Tracker .exe ...
%PY_CMD% -m PyInstaller --noconfirm "build\Payslip Tracker.spec"
if errorlevel 1 (
    echo Build failed.
    pause
    exit /b %errorlevel%
)
echo.
echo Build complete. The exe is in: dist\Payslip Tracker\
echo Config is bundled into the app build.
echo Share this folder along with input/ and output/ if needed.
pause
