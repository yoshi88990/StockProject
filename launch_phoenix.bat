@echo off
:: [PHOENIX RELIABLE LAUNCHER] v2
:: ---------------------------
subst P: /d > nul 2>&1
subst P: "C:\StockProject"

cd /d "C:\StockProject"

:: Launch Backend
start "" wscript "PHOENIX_LAUNCH_WEB.vbs"
timeout /t 2 /nobreak > nul

:: Launch Dashboard (Terminal)
start "PHOENIX_DASHBOARD" "python_embed\python.exe" "PHOENIX_DASHBOARD.py"

:: Open Browser
start "" "http://localhost:8000"

exit
