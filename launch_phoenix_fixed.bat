@echo off
title PHOENIX_LAUNCHER
:: 1. Force P: drive mapping
subst P: /d > nul 2>&1
subst P: "C:\StockProject"
if errorlevel 1 (
    echo [ERROR] Failed to map P: drive.
    pause
    exit
)

:: 2. Start Backend (Web Server) via VBS
if exist "P:\PHOENIX_LAUNCH_WEB.vbs" (
    wscript.exe "P:\PHOENIX_LAUNCH_WEB.vbs"
) else (
    echo [ERROR] P:\PHOENIX_LAUNCH_WEB.vbs not found.
)

:: 3. Wait for server
timeout /t 3 /nobreak > nul

:: 4. Start Dashboard (Terminal - Black Screen)
start "PHOENIX_DASHBOARD" cmd /k "python P:\PHOENIX_DASHBOARD.py"

:: 5. Open Web UI
start "" "http://localhost:8000"

exit
