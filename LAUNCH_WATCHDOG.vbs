Set ws = CreateObject("WScript.Shell")

' 絶対パスによる監視システム (SNIPER WATCHDOG 24H) の起動
pythonExe = """C:\Users\yoshi\AppData\Local\Python\bin\pythonw.exe"""
scriptPath = """C:\Users\yoshi\OneDrive\Weekly report\Phoenix_Protocol\SNIPER_WATCHDOG.py"""

' 完全なバックグラウンド実行（1秒周期でAIが勝手に書き換えていないかを常時監視し、復旧する）
ws.Run pythonExe & " " & scriptPath, 0, False
