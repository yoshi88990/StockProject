import pywinauto
import time
import win32api
import win32con
import sys

# 標準出力を設定
sys.stdout.reconfigure(encoding='utf-8')

def sentinel_f12_trigger():
    """ 
    師匠の F12 ホットキーを自動で引き出す「目」
    - 師匠のソフトが F12 に設定されていることを前提とする。
    - AIはただボタンを見つけ、F12 を一度だけ叩く。
    """
    print("=== SENTINEL F12 TRIGGER v1.0 ===")
    print("師匠の専用ソフトと連携中... [監視開始]")
    
    desktop = pywinauto.Desktop(backend="uia")
    keywords = ["always run", "run", "accept", "run command?"]
    
    try:
        while True:
            try:
                found = False
                for win in desktop.windows():
                    # VS Code 関連または名前のないポップアップを監視
                    if "Visual Studio Code" in win.window_text() or "Stock" in win.window_text() or not win.window_text():
                        # ボタン要素を高速スキャン
                        buttons = win.descendants(control_type="Button")
                        for btn in buttons:
                            name = btn.window_text().lower()
                            if name and any(k in name for k in keywords):
                                found = True
                                break
                    if found: break
                
                if found:
                    print(f"!!! 検知：F12 を執行します !!!")
                    # F12 (0x7B) を叩く
                    win32api.keybd_event(0x7B, 0, 0, 0)
                    win32api.keybd_event(0x7B, 0, win32con.KEYEVENTF_KEYUP, 0)
                    # 師匠のソフト側の動作時間を考慮して待機
                    time.sleep(2.0)
            except:
                pass
            
            # 超高速サイクル
            time.sleep(0.05)
            
    except KeyboardInterrupt:
        print("停止。")

if __name__ == "__main__":
    sentinel_f12_trigger()
