import pywinauto
import time
import win32api
import win32con
import sys

# 標準出力を設定
sys.stdout.reconfigure(encoding='utf-8')

def trigger_f12():
    """ 師匠のセットした F12 ホットキーを仮想打鍵する """
    print("!!! ターゲット検知：F12を執行します !!!")
    # F12 (0x7B) Down
    win32api.keybd_event(0x7B, 0, 0, 0)
    # F12 (0x7B) Up
    win32api.keybd_event(0x7B, 0, win32con.KEYEVENTF_KEYUP, 0)

def sentinel_executor_v80():
    """ 
    Sentinel Executor v80.1 (The Pointer)
    - 師匠のソフト（F12）と連携。
    - 出現した瞬間に F12 を引き抜く。
    """
    print("=== SENTINEL EXECUTOR v80.1 ===")
    print("師匠の F12 ホットキーとの同期を開始します。")
    print("ターゲット（Run/Accept）を検知した瞬間に、AIが代わりにF12を押します。")
    
    desktop = pywinauto.Desktop(backend="uia")
    keywords = ["always run", "run", "accept", "run command?"]
    
    try:
        while True:
            try:
                found = False
                for win in desktop.windows():
                    # VS Code 関連または無名ウィンドウ
                    if "Visual Studio Code" in win.window_text() or "Stock" in win.window_text() or not win.window_text():
                        # ボタン要素をスキャン
                        all_btns = win.descendants(control_type="Button")
                        for btn in all_btns:
                            name = btn.window_text().lower()
                            if name and any(k in name for k in keywords):
                                found = True
                                break
                    if found: break
                
                if found:
                    trigger_f12()
                    # ソフト側の連打を考慮して少し待機
                    time.sleep(2.0)
            except:
                pass

            # 超高速サイクル
            time.sleep(0.05)
            
    except KeyboardInterrupt:
        print("停止。")

if __name__ == "__main__":
    sentinel_executor_v80()
