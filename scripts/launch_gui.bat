@echo off
rem NanoMD Designer launcher (Windows)
rem Runs the GUI from the project virtual environment without a console window.
cd /d "%~dp0\.."

if not exist ".venv\Scripts\pythonw.exe" (
    echo Virtual environment not found. Create it first:
    echo   python -m venv .venv
    echo   .venv\Scripts\pip install -e ".[gui]"
    pause
    exit /b 1
)

start "" ".venv\Scripts\pythonw.exe" -m nanomd.gui.main
