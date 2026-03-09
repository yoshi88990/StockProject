' ==============================================================================
' 【PHOENIX STOPPER】 v1.1
' すべての守護プロセス（番犬・狙撃手）を安全に停止します。
' ==============================================================================
Set ws = CreateObject("WScript.Shell")

' WMIを使用して特定のスクリプトを実行中のpythonw.exeを探して停止
On Error Resume Next
Set objWMIService = GetObject("winmgmts:{impersonationLevel=impersonate}!\\.\root\cimv2")
Set colProcessList = objWMIService.ExecQuery("Select * from Win32_Process Where Name = 'pythonw.exe' OR Name = 'python.exe'")

count = 0
For Each objProcess in colProcessList
    cmdLine = objProcess.CommandLine
    If Not IsNull(cmdLine) Then
        If InStr(cmdLine, "ACCEPT_ALL_MINIMAL.py") > 0 Or InStr(cmdLine, "PHOENIX_IMMUNE_SYSTEM.py") > 0 Or InStr(cmdLine, "PHOENIX_MINI_MONITOR.py") > 0 Then
            objProcess.Terminate()
            count = count + 1
        End If
    End If
Next

' 完了通知
msg = "Phoenix Stop Protocol executed: " & count & " processes terminated."
ws.Popup msg, 3, "Phoenix Stopper", 64
