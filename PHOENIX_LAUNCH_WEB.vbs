' ==============================================================================
' [PHOENIX WEB DASHBOARD LAUNCHER] v1.0
' 師匠の命：スペース入りのパス問題を VBS で力技で解決する
' ==============================================================================
Set ws = CreateObject("WScript.Shell")

' 会社PCの Python Path - スペースを考慮して chr(34) で囲む
pythonw = chr(34) & "C:\Users\kanku\OneDrive\Weekly report\python_embed\pythonw.exe" & chr(34)
app_dir = chr(34) & "P:/" & chr(34)

' 起動コマンド構成
' ログが見たい場合は pythonw を python に変えて cmd /k で実行するが、
' 今回はウェブ版なので無音 (0) でバックグラウンド起動させる。
command = pythonw & " -m uvicorn PHOENIX_WEB_SERVER:app --host 0.0.0.0 --port 8000 --app-dir " & app_dir

ws.Run command, 0, False
