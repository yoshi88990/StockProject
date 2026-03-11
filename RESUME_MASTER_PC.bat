@echo off
setlocal enabledelayedexpansion
chcp 65001 > nul

:: ==============================================================================
:: [PHOENIX RESUME MASTER PC] v13.1 (2026-03-11 Revision)
:: ==============================================================================

echo [*] PHOENIX PROTOCOL: RESUME SEQUENCE INITIATED...

:: 1. subst P:
subst P: /d > nul 2>&1
set target_dir=C:\StockProject
if not exist "%target_dir%" mkdir "%target_dir%"
subst P: "%target_dir%"
echo [OK] P: Drive mapped.

:: 2. Sync
cd /d P:\
git pull origin master
echo [OK] DNA sync attempted.

:: 3. Purge
taskkill /F /IM python.exe /T > nul 2>&1
taskkill /F /IM pythonw.exe /T > nul 2>&1

:: 4. Ignition
if exist "P:\python_embed\python.exe" (
    start /min "" "P:\python_embed\python.exe" "P:\PHOENIX_MASTER_UNIFIER.py"
) else (
    start /min "" "python.exe" "P:\PHOENIX_MASTER_UNIFIER.py"
)

:: 5. Dashboard
timeout /t 2 > nul
if exist "P:\PHOENIX_LAUNCH_WEB.vbs" (
    start "" wscript.exe "P:\PHOENIX_LAUNCH_WEB.vbs"
)

echo.
echo ----------------------------------------------------
echo [COMPLETE] PHOENIX HAS RESUMED.
echo ----------------------------------------------------
timeout /t 5
exit
