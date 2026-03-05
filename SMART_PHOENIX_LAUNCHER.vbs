' ==============================================================================
' 【SMART PHOENIX LAUNCHER】 v3.0 (Zero-Japanese Pure ASCII Fix)
' ==============================================================================

Set ws = CreateObject("WScript.Shell")
Set net = CreateObject("WScript.Network")

computerName = net.ComputerName
pythonw = "C:\Users\kanku\Desktop\Weekly report\Weekly-report\python_embed\pythonw.exe"
baseDir = "C:\Users\kanku\OneDrive\Weekly report"

' --- Environment Detection ---
If computerName = "G580" Then
    profileLabel = "Office"
    watchdogScript = baseDir & "\Phoenix_Protocol\SNIPER_WATCHDOG.py"
    receptorScript = baseDir & "\Phoenix_Protocol\手術台_解剖室\02_RECEPTOR_SYNAPSE.py"
Else
    profileLabel = "Home"
    watchdogScript = baseDir & "\Phoenix_Protocol\SNIPER_WATCHDOG.py"
    receptorScript = baseDir & "\Phoenix_Protocol\手術台_解剖室\02_RECEPTOR_SYNAPSE.py"
End If

' --- Execution ---
' 1. WATCHDOG (Background)
ws.Run """" & pythonw & """ """ & watchdogScript & """", 0, False

' 2. RECEPTOR (Background)
ws.Run """" & pythonw & """ """ & receptorScript & """", 0, False

' Display Japanese Message via PowerShell to avoid VBS encoding errors
' DNA (Base64) for " 起動完了。無音で守護を開始します。"
dnaMsg = "NkxXMzVVVjVhNk01THFHNUNDNTRTaDZaK3o0NEduNWE2STZLMjQ0S1M2WmFMNWFlTDQ0R1g0NEcrNDRHVjQ0Q0M="
psCmd = "powershell -WindowStyle Hidden -Command ""$m=[System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String('6LW35YuV5a6M5LqG44CC54Sh6Z+z44Gn5a6I6K2344KS6ZaL5aeL44GX44G+44GZ44CC')); [Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms'); [System.Windows.Forms.MessageBox]::Show('PHOENIX [' + '" & profileLabel & "' + '] ' + $m, 'Phoenix Launcher')"""
ws.Run psCmd, 0, False
