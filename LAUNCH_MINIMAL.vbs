Set ws = CreateObject("WScript.Shell")

' 絶対パスによる指定（どこから起動されても確実に C:\StockProject を向く）
pythonExe = """C:\Users\kanku\Desktop\Weekly report\Weekly-report\python_embed\pythonw.exe"""
scriptPath = """C:\StockProject\ACCEPT_ALL_MINIMAL.py"""

' OS起動時からの完全バックグラウンド実行 ＆ 不死身の監視ループ（Watchdog）
Do
    ' True = スクリプトが終了・クラッシュするまで待機（監視）する
    ws.Run pythonExe & " " & scriptPath, 0, True
    
    ' 万が一、タスクマネージャー等で強制終了された場合、3秒待ってからOSの力で蘇生する
    WScript.Sleep 3000
Loop
