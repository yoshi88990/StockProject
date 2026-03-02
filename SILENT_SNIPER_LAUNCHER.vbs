Set ws = CreateObject("WScript.Shell")
' カレントディレクトリを取得して実行
currDir = ws.CurrentDirectory
ws.Run "pythonw.exe " & currDir & "\SOVEREIGN_SNIPER.py", 0, False
