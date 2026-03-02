import win32api
import win32con
import time
import pywinauto
import sys

# 標準出力を設定
sys.stdout.reconfigure(encoding='utf-8')

# F8 Virtual Key
VK_F8 = 0x77

def trigger_f8_vk(reason=""):
    """ 師匠のソフトを引き出すための F8 打鍵 """
    print(f"[{time.strftime('%H:%M:%S')}] 🔥 F8 執行: {reason}")
    win32api.keybd_event(VK_F8, 0, 0, 0)
    time.sleep(0.05)
    win32api.keybd_event(VK_F8, 0, win32con.KEYEVENTF_KEYUP, 0)

def click_bottom_right_burst(count=5):
    """ 右下端を連打する（通知消去用など） """
    width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
    height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
    # 右下のさらに端っこをターゲット
    target = (width - 10, height - 10) 
    
    print(f"[{time.strftime('%H:%M:%S')}] 🎯 右下連打執行(5連): {target}")
    orig_pos = win32api.GetCursorPos()
    
    try:
        for _ in range(count):
            win32api.SetCursorPos(target)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            time.sleep(0.05)
    finally:
        # マウスを元の位置に瞬時に戻す
        win32api.SetCursorPos(orig_pos)

def main():
    print("=== FINAL SENTINEL v98.0 ===")
    print("1. [自動] ボタン検知(Always run/Run/Accept)で即座に F8")
    print("2. [定時] 60秒ごとに『独立して』F8 ＋ 右下5連打")
    print("---------------------------------------------")

    desktop = pywinauto.Desktop(backend="uia")
    keywords = ["always run", "run", "accept", "run command?"]
    
    # 定時実行用の専用タイマー（ボタン検知にリセットされない）
    last_periodic_time = time.time()
    
    try:
        while True:
            current_time = time.time()
            
            # --- 1. 定時実行（1分ごと厳守） ---
            if current_time - last_periodic_time >= 60:
                print("--- 定時パルス執行 (1分経過) ---")
                trigger_f8_vk("1分定時パルス")
                click_bottom_right_burst(5)
                last_periodic_time = current_time

            # --- 2. ボタン検知（即時） ---
            try:
                found = False
                for win in desktop.windows():
                    title = win.window_text()
                    if "Visual Studio Code" in title or "Stock" in title or not title:
                        buttons = win.descendants(control_type="Button")
                        for btn in buttons:
                            name = btn.window_text().lower()
                            if name and any(k in name for k in keywords):
                                found = True
                                break
                    if found: break
                
                if found:
                    trigger_f8_vk("ボタン検知(即時)")
                    # 検知後の連打防止クールダウン
                    time.sleep(2.0)
            except:
                pass

            # 超高速スキャン間隔
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n停止しました。")

if __name__ == "__main__":
    main()
