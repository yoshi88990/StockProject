Set ws = CreateObject("WScript.Shell")
pythonw = "C:\Users\kanku\Desktop\Weekly report\Weekly-report\python_embed\pythonw.exe"
script = "C:\StockProject\PHOENIX_DASHBOARD.py"
' Run with window style 7 (minimized)
ws.Run """" & pythonw & """ """ & script & """", 7, False
