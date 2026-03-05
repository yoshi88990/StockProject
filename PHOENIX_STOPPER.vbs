' ==============================================================================
' 【PHOENIX STOPPER】 v1.0
' すべての守護プロセス（番犬・狙撃手）を安全に停止します。
' ==============================================================================

Set ws = CreateObject("WScript.Shell")

' WMIを使用して特定のスクリプトを実行中のpythonw.exeを探して停止
Set objWMIService = GetObject("winmgmts:{impersonationLevel=impersonate}!\\.\root\cimv2")
Set colProcessList = objWMIService.ExecQuery("Select * from Win32_Process Where Name = 'pythonw.exe'")

count = 0
For Each objProcess in colProcessList
    cmdLine = objProcess.CommandLine
    If Not IsNull(cmdLine) Then
        If InStr(cmdLine, "SNIPER_WATCHDOG.py") > 0 Or InStr(cmdLine, "02_RECEPTOR_SYNAPSE.py") > 0 Then
            objProcess.Terminate()
            count = count + 1
        End If
    End If
Next

' 完了通知 (PowerShell経由で日本語を表示)
If count > 0 Then
    msg = "PHOENIX の守護を停止しました。すべてのプロセスは安全に終了しました。"
Else
    msg = "稼働中の PHOENIX プロセスは見つかりませんでした。"
End If

dnaMsg = "PHOENIX ̂錇~܂BׂẴvZX͉SɏI܂B"
' 日本語を安全に表示するためのPowerShellコマンド
psCmd = "powershell -WindowStyle Hidden -Command ""[Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms'); [System.Windows.Forms.MessageBox]::Show('" & msg & "', 'Phoenix Stopper')"""
ws.Run psCmd, 0, False
