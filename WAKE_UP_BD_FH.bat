@echo off
subst P: /d > nul 2>&1
subst P: C:\StockProject
echo [*] Waking up Phoenix Agents (BD, FH, DNA)...

:: 迷わない。空の引用符を最初に置き、EXEと引数を別々に囲う。
start "" "P:\python_embed\python.exe" "P:\ACCEPT_ALL_MINIMAL.py"
start "" "P:\python_embed\python.exe" "P:\PHOENIX_HUMILITY_SENSOR.py"
start "" "P:\python_embed\python.exe" "P:\PHOENIX_SENTINEL.py"
start "" "P:\python_embed\python.exe" "P:\PHOENIX_ANALYST_CORE.py"
start "" "P:\python_embed\python.exe" "P:\PHOENIX_DNA_SYNCHRONIZER.py"

echo [OK] Execution complete. No popups expected.
timeout /t 3
exit
