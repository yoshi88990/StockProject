Set ws = CreateObject("WScript.Shell")
pythonPath = "C:\Users\yoshi\AppData\Local\Python\pythoncore-3.14-64\python.exe"
scriptPath = "C:\Users\yoshi\OneDrive\Weekly report\Phoenix_Protocol\PHOENIX_DASHBOARD_HOME.py"
command = "cmd /c color 0F && " & chr(34) & pythonPath & chr(34) & " " & chr(34) & scriptPath & chr(34)
' 1 = Activate and display window
ws.Run command, 1, False
