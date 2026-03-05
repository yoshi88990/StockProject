Set ws = CreateObject("WScript.Shell")
pythonExe = "C:\Users\kanku\Desktop\Weekly report\Weekly-report\python_embed\pythonw.exe"
scriptPath = "C:\StockProject\PHOENIX_COMPUTE_NODE.py"
ws.Run """" & pythonExe & """ """ & scriptPath & """", 0, False
