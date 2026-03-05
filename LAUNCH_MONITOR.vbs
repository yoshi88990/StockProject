Set ws = CreateObject("WScript.Shell")
' PowerShellを使用して極小モニター(.ps1)を完全に無音で起動
psPath = "powershell.exe -WindowStyle Hidden -ExecutionPolicy Bypass -File ""C:\Users\kanku\OneDrive\Weekly report\Phoenix_Protocol\PHOENIX_MINI_MONITOR.ps1"""

ws.Run psPath, 0, False
