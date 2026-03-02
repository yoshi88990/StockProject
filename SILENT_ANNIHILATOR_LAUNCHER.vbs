Set ws = CreateObject("WScript.Shell")
currDir = ws.CurrentDirectory
ws.Run "pythonw.exe " & currDir & "\BOTTOM_RIGHT_ANNIHILATOR.py", 0, False
