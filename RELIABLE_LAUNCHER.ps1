$py_win = "C:\Users\yoshi\AppData\Local\Python\bin\pythonw.exe"
$py_con = "C:\Users\yoshi\AppData\Local\Python\bin\python.exe"

$scripts = @(
    "c:\Users\yoshi\OneDrive\Weekly report\Phoenix_Protocol\ACCEPT_ALL_MINIMAL.py",
    "c:\Users\yoshi\OneDrive\Weekly report\commander.py",
    "c:\Users\yoshi\OneDrive\Weekly report\Phoenix_Protocol\SNIPER_WATCHDOG.py",
    "c:\Users\yoshi\OneDrive\Weekly report\Phoenix_Protocol\手術台_解剖室\02_RECEPTOR_SYNAPSE.py"
)

# 1-4. バックグラウンド起動
foreach ($s in $scripts) {
    Start-Process $py_win -ArgumentList "`"$s`""
    Start-Sleep -Milliseconds 500
}

# 5. ダッシュボード起動 (v10.1 静寂潜伏モード)
$db = "c:\Users\yoshi\OneDrive\Weekly report\Phoenix_Protocol\PHOENIX_DASHBOARD_HOME.py"
Start-Process $py_con -ArgumentList "`"$db`""

