Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

$form = New-Object Windows.Forms.Form
$form.Text = "Phoenix Mini"
$form.Size = New-Object Drawing.Size(220, 70)
$form.FormBorderStyle = "None"
$form.TopMost = $true
$form.BackColor = [Drawing.Color]::FromArgb(10, 10, 10)
$form.StartPosition = "Manual"
$form.Location = New-Object Drawing.Point(($([System.Windows.Forms.Screen]::PrimaryScreen.WorkingArea.Width) - 240), 40)

# ドラッグ移動
$form.add_MouseDown({
    $script:dragging = $true
    $script:originalPos = [System.Windows.Forms.Cursor]::Position
    $script:originalFormPos = $form.Location
})
$form.add_MouseMove({
    if ($script:dragging) {
        $delta = [System.Drawing.Point]::Subtract([System.Windows.Forms.Cursor]::Position, $script:originalPos)
        $form.Location = [System.Drawing.Point]::Add($script:originalFormPos, $delta)
    }
})
$form.add_MouseUp({ $script:dragging = $false })

# 枠線
$panel = New-Object Windows.Forms.Panel
$panel.Dock = "Fill"
$panel.BorderStyle = "FixedSingle"
$form.Controls.Add($panel)

# ステータスLED
$led = New-Object Windows.Forms.Label
$led.Location = New-Object Drawing.Point(10, 15)
$led.Size = New-Object Drawing.Size(10, 10)
$led.BackColor = [Drawing.Color]::DarkGray
$panel.Controls.Add($led)

# ステータステキスト
$statusLabel = New-Object Windows.Forms.Label
$statusLabel.Text = "PHOENIX: OFF"
$statusLabel.ForeColor = [Drawing.Color]::Gray
$statusLabel.Font = New-Object Drawing.Font("Segoe UI", 8)
$statusLabel.Location = New-Object Drawing.Point(25, 13)
$statusLabel.AutoSize = $true
$panel.Controls.Add($statusLabel)

# ボタン: START
$btnStart = New-Object Windows.Forms.Button
$btnStart.Text = "▶"
$btnStart.Size = New-Object Drawing.Size(25, 20)
$btnStart.Location = New-Object Drawing.Point(155, 10)
$btnStart.FlatStyle = "Flat"
$btnStart.FlatAppearance.BorderSize = 0
$btnStart.ForeColor = [Drawing.Color]::Cyan
$btnStart.Font = New-Object Drawing.Font("Arial", 8)
$btnStart.add_Click({
    Start-Process "cscript.exe" "//B ""C:\Users\kanku\OneDrive\Weekly report\Phoenix_Protocol\SMART_PHOENIX_LAUNCHER.vbs"""
})
$panel.Controls.Add($btnStart)

# ボタン: STOP
$btnStop = New-Object Windows.Forms.Button
$btnStop.Text = "■"
$btnStop.Size = New-Object Drawing.Size(25, 20)
$btnStop.Location = New-Object Drawing.Point(185, 10)
$btnStop.FlatStyle = "Flat"
$btnStop.FlatAppearance.BorderSize = 0
$btnStop.ForeColor = [Drawing.Color]::DeepPink
$btnStop.Font = New-Object Drawing.Font("Arial", 8)
$btnStop.add_Click({
    Start-Process "cscript.exe" "//B ""C:\Users\kanku\OneDrive\Weekly report\Phoenix_Protocol\PHOENIX_STOPPER.vbs"""
})
$panel.Controls.Add($btnStop)

# 下段バー
$bar = New-Object Windows.Forms.Label
$bar.BackColor = [Drawing.Color]::FromArgb(40, 40, 40)
$bar.Location = New-Object Drawing.Point(10, 38)
$bar.Size = New-Object Drawing.Size(180, 1)
$panel.Controls.Add($bar)

# 閉じる小ボタン
$btnClose = New-Object Windows.Forms.Label
$btnClose.Text = "×"
$btnClose.ForeColor = [Drawing.Color]::FromArgb(60, 60, 60)
$btnClose.Location = New-Object Drawing.Point(205, 5)
$btnClose.Size = New-Object Drawing.Size(10, 10)
$btnClose.Cursor = [System.Windows.Forms.Cursors]::Hand
$btnClose.add_Click({ $form.Close() })
$panel.Controls.Add($btnClose)

# バージョン等
$infoLabel = New-Object Windows.Forms.Label
$infoLabel.Text = "SYSTEM READY"
$infoLabel.ForeColor = [Drawing.Color]::FromArgb(80, 80, 80)
$infoLabel.Font = New-Object Drawing.Font("Consolas", 7)
$infoLabel.Location = New-Object Drawing.Point(10, 45)
$infoLabel.AutoSize = $true
$panel.Controls.Add($infoLabel)

# 監視タイマー
$timer = New-Object Windows.Forms.Timer
$timer.Interval = 2000
$timer.add_Tick({
    $res = Get-WmiObject Win32_Process -Filter "Name='pythonw.exe'" | Select-Object -ExpandProperty CommandLine -ErrorAction SilentlyContinue
    $isWatchdog = $res -like "*SNIPER_WATCHDOG.py*"
    $isReceptor = $res -like "*02_RECEPTOR_SYNAPSE.py*"

    if ($isWatchdog -and $isReceptor) {
        $statusLabel.Text = "PHOENIX: ACTIVE"
        $statusLabel.ForeColor = [Drawing.Color]::SpringGreen
        $led.BackColor = [Drawing.Color]::SpringGreen
        $infoLabel.Text = "WATCHING: OK"
    } elseif ($isWatchdog -or $isReceptor) {
        $statusLabel.Text = "PHOENIX: PARTIAL"
        $statusLabel.ForeColor = [Drawing.Color]::Gold
        $led.BackColor = [Drawing.Color]::Gold
        $infoLabel.Text = "SYNC ERROR"
    } else {
        $statusLabel.Text = "PHOENIX: OFF"
        $statusLabel.ForeColor = [Drawing.Color]::Gray
        $led.BackColor = [Drawing.Color]::DarkGray
        $infoLabel.Text = "IDLE"
    }
})
$timer.Start()

$form.ShowDialog()
