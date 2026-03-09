Set ws = CreateObject("WScript.Shell")
pythonExe = "P:\python_embed\pythonw.exe"
scriptPath = "P:\PHOENIX_STOCK_ANALYST.py"
ws.Run """" & pythonExe & """ """ & scriptPath & """", 0, False
