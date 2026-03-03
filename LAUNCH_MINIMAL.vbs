Set ws = CreateObject("WScript.Shell")
' 実行パスにスペースが含まれるため、全体をダブルクォーテーションで囲む
currDir = ws.CurrentDirectory
pythonExe = """C:\Users\kanku\Desktop\Weekly report\Weekly-report\python_embed\pythonw.exe"""
scriptPath = """" & currDir & "\ACCEPT_ALL_MINIMAL.py"""

' 完全なバックグラウンド実行（黒い窓なし）
ws.Run pythonExe & " " & scriptPath, 0, False
