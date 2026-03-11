@echo off
title PHOENIX_REBIRTH
:: -----------------------------------------------------------------------------
:: PHOENIX PROTOCOL: LAUNCH SEQUENCE (RELIABLE EDITION)
:: -----------------------------------------------------------------------------

:: 1. Force P: Drive mapping
subst P: /d > nul 2>&1
subst P: "C:\StockProject"
if errorlevel 1 (
    echo [!] ERROR: Failed to map P: drive to C:\StockProject
    pause
    exit
)
echo [OK] P: Drive mapped.

:: 2. Start Backend (Hidden Web Server)
echo [*] Starting Web Server...
if exist "P:\PHOENIX_LAUNCH_WEB.vbs" (
    start /b wscript.exe "P:\PHOENIX_LAUNCH_WEB.vbs"
) else (
    echo [!] ERROR: P:\PHOENIX_LAUNCH_WEB.vbs not found.
    pause
    exit
)

:: 3. Give the server time to pulse
timeout /t 3 /nobreak > nul

:: 4. Start Dashboard (Terminal - Visible/Black)
echo [*] Starting Terminal Dashboard...
if exist "P:\PHOENIX_DASHBOARD.py" (
    start "PHOENIX DASHBOARD" cmd /k "P:\python_embed\python.exe P:\PHOENIX_DASHBOARD.py"
)

:: 5. Launch User Interface
echo [*] Launching Web UI...
start http://localhost:8000

echo [COMPLETE] PHOENIX HAS AWAKENED.
exit
