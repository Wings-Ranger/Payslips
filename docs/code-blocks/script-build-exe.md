# script: build_exe.bat

**File:** `scripts/build_exe.bat`

## What It Is

`build_exe.bat` is a Windows batch script that packages `src/payslip_tracker.py` into a standalone `.exe` using [PyInstaller](https://pyinstaller.org). The resulting executable can be given to end users who do not have Python installed — they double-click the `.exe` instead of running the batch file.

## Code Block

```bat
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
```

## How to Re-Implement

1. `cd /d %~dp0` changes to the directory where the batch file lives (`%~dp0` is the drive and path of the script itself). This makes all relative paths predictable regardless of where you launch the script from.
2. `--noconfirm --clean` prevents PyInstaller from asking questions and removes stale build artefacts before starting.
3. `--name "Payslip Tracker"` sets the name of both the exe and the output folder.
4. `--distpath dist` puts the finished exe folder inside `dist/` at the project root; `--workpath build\pyinstaller` keeps intermediate build files out of the root.
5. `if %errorlevel% neq 0` checks whether PyInstaller reported an error and exits early with a visible message so the build failure is not silently swallowed.
6. The final message reminds the packager to bundle `input/`, `output/`, and `src/config.json` alongside the exe — those files are not embedded by PyInstaller.

### Prerequisites

```powershell
pip install pyinstaller
```

### Running

Double-click `scripts/build_exe.bat`, or from a terminal at the project root:

```bat
scripts\build_exe.bat
```

The distributable is placed in `dist\Payslip Tracker\`. Share the entire `dist\Payslip Tracker\` folder together with the `input\`, `output\`, and `src\config.json` files.

> **Note:** PyInstaller is **not** listed in `docs/requirements.txt` because it is only needed to create a distributable — it is not required to run the tool from source. Install it separately in your development environment before running this script.
