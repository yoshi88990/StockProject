import keyboard
import pywinauto
import time
import win32api
import sys

sys.stdout.reconfigure(encoding='utf-8')

# 師匠から継承した急所座標
MASTER_RUN_COORD = (1319, 236)
MASTER_ACCEPT_COORD = (1292, 600)

def execute_annihilation():
    """ 必殺の5連撃を、指定座標とAlt+Enterで実行する """
    print("!!! 消滅プロトコル：発動 !!!")
    
    # 1. 物理的なAlt+Enter送信
    keyboard.press_and_release('alt+enter')
    
    # 2. 師匠から教わった急所座標を叩く (5回制限)
    for _ in range(5):
        # RUN座標
        win32api.SetCursorPos(MASTER_RUN_COORD)
        win32api.mouse_event(2, 0, 0, 0, 0) # Down
        win32api.mouse_event(4, 0, 0, 0, 0) # Up
        
        # Accept座標
        win32api.SetCursorPos(MASTER_ACCEPT_COORD)
        win32api.mouse_event(2, 0, 0, 0, 0)
        win32api.mouse_event(4, 0, 0, 0, 0)
        
        time.sleep(0.02)
    print("狙撃完了。")

def start_god_mode():
    print("=== SOVEREIGN GOD MODE v70.0 ===")
    print("1. [手動] F12 を押すと即座に Alt+Enter + 座標狙撃を実行")
    print("2. [自動] 画面に Run/Accept が出たら AI が自動で F12 を押す")
    print("3. [停止] ESC を長押しするとプログラムを終了")
    print("---------------------------------")

    # 手動ホットキーの登録
    keyboard.add_hotkey('f12', execute_annihilation)

    desktop = pywinauto.Desktop(backend="uia")
    keywords = ["always run", "run", "accept", "run command?"]

    try:
        while True:
            # ESCで終了
            if keyboard.is_pressed('esc'):
                print("システムを終了します。")
                break
                
            # 自動監視モード
            try:
                found = False
                for win in desktop.windows():
                    # VS Code またはそれに関連する窓を監視
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
                    print("!!! 自動検知：敵影を確認 !!!")
                    execute_annihilation()
                    time.sleep(2.0) # 連続発動を防止
            except:
                pass

            time.sleep(0.1)

    except Exception as e:
        print(f"致命的エラー: {e}")

if __name__ == "__main__":
    start_god_mode()
