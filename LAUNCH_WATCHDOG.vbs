Set ws = CreateObject("WScript.Shell")
pythonExe = "C:\Users\kanku\Desktop\Weekly report\Weekly-report\python_embed\pythonw.exe"
scriptPath = "C:\StockProject\SNIPER_WATCHDOG.py"
ws.Run """" & pythonExe & """ """ & scriptPath & """", 0, False
