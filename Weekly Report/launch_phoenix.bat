@echo off
:: PHOENIX DASHBOARD LAUNCH SEQUENCE
:: ---------------------------------
:: 1. Subst P: Drive
subst P: /d > nul 2>&1
subst P: "C:\StockProject"

:: 2. Start Web Server (Backend)
start /min "" "P:\PHOENIX_LAUNCH_WEB.vbs"
timeout /t 2 /nobreak > nul

:: 3. Start Terminal Dashboard (Visible Black Screen)
start "PHOENIX DASHBOARD" cmd /k "python P:\PHOENIX_DASHBOARD.py"

:: 4. Open Web UI (Browser)
start http://localhost:8000

echo [COMPLETE] PHOENIX HAS AWAKENED.
exit
