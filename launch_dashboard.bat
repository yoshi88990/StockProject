@echo off
subst P: /d > nul 2>&1
subst P: "C:\StockProject"
cd /d P:\
start /min "" "P:\PHOENIX_LAUNCH_WEB.vbs"
timeout /t 2 /nobreak > nul
start http://localhost:8000
start "PHOENIX DASHBOARD" cmd /k "python P:\PHOENIX_DASHBOARD.py"
exit
