Dim objShell
Set objShell = WScript.CreateObject("WScript.Shell")

' 完全にバックグラウンド(第2引数=0)ではなく、最小化状態(第2引数=7)で起動する
' 0 = 非表示 (Hidden) -> 信号が届かない
' 7 = 最小化で非アクティブ (Minimized, Inactive) -> タスクバーにだけ表示され邪魔しない
objShell.Run "cmd.exe /c python ULTIMATE_COORDINATE_SNIPER.py", 7, False
