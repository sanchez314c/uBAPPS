@echo off
setlocal enabledelayedexpansion

REM ============================================
REM uB Suite - Windows Source Runner
REM
REM NOTE: uB Suite is designed for Ubuntu/Linux.
REM GTK AppIndicator is not supported on Windows.
REM Most apps will NOT work on Windows without
REM significant modifications.
REM ============================================

echo.
echo ============================================
echo    uB Suite - Windows Source Runner
echo ============================================
echo.

if "%1"=="" goto usage

echo [CHECK] Verifying dependencies...

where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not installed!
    echo   Install from: https://python.org
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version 2^>^&1') do echo [OK] %%i

echo.
echo [WARN] uB Suite is designed for Ubuntu/Linux.
echo   GTK AppIndicator is not natively supported on Windows.
echo.

set APP=%1

if /i "%APP%"=="ubcpu" (set FOLDER=uBCPU& set SCRIPT=ubcpu.py)
if /i "%APP%"=="ubdisk" (set FOLDER=uBDISK& set SCRIPT=ubdisk.py)
if /i "%APP%"=="ubnet" (set FOLDER=uBNET& set SCRIPT=ubnet.py)
if /i "%APP%"=="ubres" (set FOLDER=uBRES& set SCRIPT=ubres.py)
if /i "%APP%"=="ubtemp" (set FOLDER=uBTEMP& set SCRIPT=ubtemp.py)
if /i "%APP%"=="ubtime" (set FOLDER=uBTIME& set SCRIPT=ubtime.py)
if /i "%APP%"=="ubweat" (set FOLDER=uBWEAT& set SCRIPT=ubweat.py)

if not defined FOLDER (
    echo [ERROR] Unknown app: %APP%
    goto usage
)

if not exist "%FOLDER%\%SCRIPT%" (
    echo [ERROR] Script not found: %FOLDER%\%SCRIPT%
    pause
    exit /b 1
)

echo [START] Launching %FOLDER%...
python "%FOLDER%\%SCRIPT%"
goto end

:usage
echo Usage: run-source-windows.bat ^<app-name^>
echo.
echo Available apps:
echo   ubcpu   - CPU usage monitor
echo   ubdisk  - Disk I/O bandwidth monitor
echo   ubnet   - Network bandwidth monitor
echo   ubres   - Display resolution switcher
echo   ubtemp  - Hardware temperature monitor
echo   ubtime  - World clock ^& timezones
echo   ubweat  - Weather display
echo.
echo Example: run-source-windows.bat ubcpu
echo.
echo NOTE: uB Suite is designed for Ubuntu/Linux.

:end
endlocal
