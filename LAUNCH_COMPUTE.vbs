Set ws = CreateObject("WScript.Shell")
pythonExe = "P:\python_embed\pythonw.exe"
scriptPath = "P:\PHOENIX_COMPUTE_NODE.py"
ws.Run """" & pythonExe & """ """ & scriptPath & """", 0, False
