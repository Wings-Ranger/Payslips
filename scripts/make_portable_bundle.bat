@echo off
setlocal

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
  echo Install Python, then re-run this script.
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

echo Building self-contained executable...
%PY_CMD% -m PyInstaller --noconfirm "build\Payslip Tracker.spec"
if errorlevel 1 (
  echo Build failed.
  pause
  exit /b %errorlevel%
)

set "PORTABLE_DIR=portable\Payslip Tracker Portable"

if exist "%PORTABLE_DIR%" rmdir /s /q "%PORTABLE_DIR%"
mkdir "%PORTABLE_DIR%"

echo Copying runtime files...
xcopy /e /i /y "dist\Payslip Tracker" "%PORTABLE_DIR%\Payslip Tracker" >nul

if not exist "%PORTABLE_DIR%\input" mkdir "%PORTABLE_DIR%\input"
if not exist "%PORTABLE_DIR%\output" mkdir "%PORTABLE_DIR%\output"

if exist "ui_theme.json" copy /y "ui_theme.json" "%PORTABLE_DIR%\ui_theme.json" >nul

copy /y "Process Payslips.bat" "%PORTABLE_DIR%\Run Payslip Tracker.bat" >nul

echo.
echo Portable bundle ready:
echo   %PORTABLE_DIR%
echo.
echo Share this folder directly from USB.
echo End users can run: Run Payslip Tracker.bat
pause