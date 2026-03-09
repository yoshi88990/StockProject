@echo off
set "PYTHON=C:\Users\kanku\OneDrive\Weekly report\python_embed\python.exe"
set "PYTHONW=C:\Users\kanku\OneDrive\Weekly report\python_embed\pythonw.exe"
set "ROOT=C:\Users\kanku\OneDrive\Weekly report"
set "PROTOCOL=%ROOT%\Phoenix_Protocol"

echo [PHOENIX] 部隊起動 (b to g) ...

:: b. 機械打ち(固定)
start /b "" "%PYTHONW%" "%ROOT%\ACCEPT_ALL_MINIMAL.py"
:: c. 司令 (Commander)
start /b "" "%PYTHONW%" "%ROOT%\commander.py"
:: d. 謙虚監視 (Humility)
start /b "" "%PYTHONW%" "%PROTOCOL%\PHOENIX_HUMILITY_SENSOR.py"
:: e. 受容接続 (Receptor)
start /b "" "%PYTHONW%" "%PROTOCOL%\PHOENIX_DNA_SYNCHRONIZER.py"
:: f. 四半期監視 (Sentinel)
start /b "" "%PYTHONW%" "%PROTOCOL%\PHOENIX_SENTINEL.py"
:: g. 深層解析 (Analyst)
start /b "" "%PYTHONW%" "%PROTOCOL%\PHOENIX_ANALYST_CORE.py"

echo [PHOENIX] 全部隊・沈黙潜伏完了。
ping 127.0.0.1 -n 3 >nul

:: Dashboard 起動
start "" "%PYTHON%" "%PROTOCOL%\PHOENIX_DASHBOARD_HOME.py"
exit
