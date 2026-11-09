@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo [SETUP] Creating Python environment and installing pyserial...
    py -m venv .venv
    if errorlevel 1 exit /b 1
    ".venv\Scripts\python.exe" -m pip install pyserial
    if errorlevel 1 exit /b 1
)

if "%~1"=="list" (
    ".venv\Scripts\python.exe" record_ppg.py --list-ports
    exit /b %ERRORLEVEL%
)

if "%~1"=="" (
    echo Usage: start_windows.bat list
    echo        start_windows.bat COM5 [seconds]
    echo Example: start_windows.bat COM5 30
    exit /b 1
)

if "%~2"=="" (
    ".venv\Scripts\python.exe" record_ppg.py --port "%~1"
) else (
    ".venv\Scripts\python.exe" record_ppg.py --port "%~1" --seconds "%~2"
)
