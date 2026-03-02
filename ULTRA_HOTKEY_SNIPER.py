import win32api
import win32con
import time
import keyboard
import pywinauto
import sys

# 標準出力をUTF-8に設定
sys.stdout.reconfigure(encoding='utf-8')

# 師匠の教えた聖なる座標
MASTER_RUN_COORD = (1319, 236)
MASTER_ACCEPT_COORD = (1292, 600)

def fire_annihilation(reason=""):
    """ 消滅連撃：Alt+Enter + 座標狙撃 (5連撃) """
    if reason:
        print(f"【執行：{reason}】")
    
    # 物理的な Alt+Enter 送信
    keyboard.press_and_release('alt+enter')
    
    # 5連撃の掟
    for _ in range(5):
        win32api.SetCursorPos(MASTER_RUN_COORD)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        
        win32api.SetCursorPos(MASTER_ACCEPT_COORD)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
        time.sleep(0.01)

def main():
    print("=== SPEED DEMON SNIPER v73.0 ===")
    print("1. [F12] で手動発動")
    print("2. ターゲット検知で【自動】最速発動")
    print("3. [ESC長押し] で終了")
    print("--------------------------------")

    # 前回のキー状態をクリア
    win32api.GetAsyncKeyState(0x7B) # F12 = 0x7B

    desktop = pywinauto.Desktop(backend="uia")
    keywords = ["always run", "run", "accept", "run command?"]

    try:
        while True:
            # 1. ESC終了チェック
            if win32api.GetAsyncKeyState(0x1B) & 0x8000: # ESC
                print("停止します。")
                break

            # 2. 手動発動チェック (F12)
            if win32api.GetAsyncKeyState(0x7B) & 0x8000:
                fire_annihilation("手動：F12")
                while win32api.GetAsyncKeyState(0x7B) & 0x8000:
                    time.sleep(0.01)

            # 3. 自動検知・最速執行
            try:
                found = False
                for win in desktop.windows():
                    title = win.window_text()
                    if "Visual Studio Code" in title or "Stock" in title or not title:
                        # 高速スキャンのために descendant(control_type='Button') を直接叩く
                        btns = win.descendants(control_type="Button")
                        for btn in btns:
                            name = btn.window_text().lower()
                            if name and any(k in name for k in keywords):
                                found = True
                                break
                    if found: break
                
                if found:
                    fire_annihilation("自動検知")
                    time.sleep(1.5) # 瞬時の重複発動を防止
            except:
                pass

            # 監視ループの間隔（極短）
            time.sleep(0.05)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
