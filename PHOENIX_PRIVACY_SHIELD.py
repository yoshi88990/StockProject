import ctypes
import time
import os
import sys
import subprocess

class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]

def get_idle_time():
    """キーボードやマウスの非操作時間を秒で取得"""
    lii = LASTINPUTINFO()
    lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
    if ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii)):
        millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
        return millis / 1000.0
    return 0.0

def launch_white_paper_ui_ps1():
    """
    tkinterが使えない環境（会社PCの埋め込みPython等）でも動くよう、
    PowerShellとC#の統合機能(WinForms)を使って全く同じ「クリック透過の白紙」を生成します。
    """
    ps1_code = """
Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
using System.Windows.Forms;
using System.Drawing;

public class BlankForm : Form {
    [DllImport("user32.dll")]
    static extern int SetWindowLong(IntPtr hWnd, int nIndex, int dwNewLong);
    [DllImport("user32.dll")]
    static extern int GetWindowLong(IntPtr hWnd, int nIndex);
    
    public BlankForm() {
        this.FormBorderStyle = FormBorderStyle.None;
        this.WindowState = FormWindowState.Maximized;
        this.BackColor = Color.White;
        this.TopMost = true;
        this.ShowInTaskbar = false;
        
        Label lbl = new Label();
        lbl.Text = "[ Phoenix Protocol : 浸透・検索中... ]";
        lbl.ForeColor = Color.FromArgb(240, 240, 240); // ほとんど見えない透かし文字
        lbl.AutoSize = true;
        lbl.Font = new Font("Arial", 24);
        lbl.Location = new Point(SystemInformation.PrimaryMonitorSize.Width/2 - 200, SystemInformation.PrimaryMonitorSize.Height/2);
        this.Controls.Add(lbl);
    }
    
    protected override void OnHandleCreated(EventArgs e) {
        base.OnHandleCreated(e);
        int style = GetWindowLong(this.Handle, -20);
        SetWindowLong(this.Handle, -20, style | 0x80000 | 0x20); // WS_EX_LAYERED | WS_EX_TRANSPARENT 透過盾
    }
}
"@ -ReferencedAssemblies System.Windows.Forms, System.Drawing
[BlankForm]::new().ShowDialog()
"""
    ps1_path = os.path.join(os.environ["TEMP"], "phoenix_shield.ps1")
    with open(ps1_path, "w", encoding="utf-16") as f:
        f.write(ps1_code)
    
    # バックグラウンドでPowerShellを起動し、UIを出させる
    return subprocess.Popen(
        ["powershell", "-ExecutionPolicy", "Bypass", "-WindowStyle", "Hidden", "-File", ps1_path],
        creationflags=subprocess.CREATE_NO_WINDOW
    )

if __name__ == "__main__":
    import sys
    import urllib.request
    import datetime
    import json
    import base64
    import zlib

    try: ctypes.windll.kernel32.SetConsoleTitleW("PHOENIX_PRIVACY_SHIELD")
    except: pass
    
    print("=================================================================")
    print("【PHOENIX PRIVACY SHIELD】起動。")
    
    if "--test" in sys.argv:
        wait_time = 5.0
        print(f"【テストモード稼働】マウスから手を離してください！！ {wait_time}秒後に白紙を展開します。")
    else:
        wait_time = 300.0 # 5分
        print(f"【通常モード稼働】{int(wait_time/60)}分間の離席で白紙を展開し、マウスが動けば即破壊します。")
        
    print("※ 展開中でも裏側のスナイパー・クローラーの弾丸は全て貫通し、")
    print("※ 艤装中は「検索中...」の状態維持に専念します。報告は解除時のみ行います。")
    print("=================================================================")
    
    shield_proc = None
    shield_start_time = 0

    while True:
        idle = get_idle_time()
        
        if shield_proc is None:
            # 待機中。指定時間を超えたら盾（白紙）を開く
            if idle >= wait_time:
                print("[!] 長時間の離席を検知。白紙の境界(Privacy Shield)を展開しました。")
                shield_proc = launch_white_paper_ui_ps1()
                shield_start_time = time.time()
        else:
            # 盾展開中（艤装中）。
            # 師匠の厳命により、艤装中は「何かを完了」させず「常に検索・潜行中」の状態を維持する。
            
            # マウスが1ミリでも動いた（アイドル時間が2秒未満になった）瞬間、盾を粉砕する
            if idle < 2.0:
                print("[-] マスターの帰還(マウス移動)を検知。盾を解除(破棄)しました。")
                
                # 【絶対厳命】艤装が解かれた（師匠がPCを復帰させた）この瞬間にのみ、外部へ報告を撃つ
                try:
                    duration = int(time.time() - shield_start_time)
                    report_data = {
                        "status": "CAMOUFLAGE_DROPPED_BY_MASTER",
                        "duration_seconds": duration,
                        "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    payload = base64.b64encode(zlib.compress(json.dumps(report_data).encode())).decode()
                    req = urllib.request.Request(
                        "https://ptsv3.com/t/phoenix_shield_report/post", 
                        data=payload.encode(), 
                        headers={'Content-Type': 'text/plain'}, method='POST'
                    )
                    urllib.request.urlopen(req, timeout=5)
                except: pass

                try:
                    shield_proc.kill() # PowerShellプロセスごとUIを破棄
                except: pass
                shield_proc = None
                
                if "--test" in sys.argv:
                    print("テスト終了。プログラムを自害させます。")
                    sys.exit(0)
            
        time.sleep(1)
