import keyboard
import pywinauto
import time
import sys
import win32api

sys.stdout.reconfigure(encoding='utf-8')

def trigger_action():
    """
    師匠が F12 を押した瞬間に発動するマクロ部隊。
    1. Alt+Enter キーを送信。
    2. 師匠直伝の座標 (RUN & Accept) を 5連打。
    """
    print("!!! F12 鍵動: 必殺連撃開始 !!!")
    
    # 1. キーボード・ショートカット送信
    keyboard.press_and_release('alt+enter')
    
    # 2. 聖なる座標への 5連打 (師匠の掟)
    # RUN座標 (修正後)
    run_coord = (1319, 236)
    # Accept座標
    accept_coord = (1292, 600)
    
    for _ in range(5):
        win32api.SetCursorPos(run_coord)
        win32api.mouse_event(2, 0, 0, 0, 0) # Left Down
        win32api.mouse_event(4, 0, 0, 0, 0) # Left Up
        
        win32api.SetCursorPos(accept_coord)
        win32api.mouse_event(2, 0, 0, 0, 0)
        win32api.mouse_event(4, 0, 0, 0, 0)
        
        time.sleep(0.01)
    
    print("連撃完了。静寂に戻ります。")

def start_hotkey_service():
    print("ホットキー防衛システム v1.0 起動中...")
    print("【F12】キーで Alt+Enter + 精密狙撃が発動します。")
    print("(終了するにはこのウィンドウを閉じるか Ctrl+C)")

    # F12 ホットキーを登録
    keyboard.add_hotkey('f12', trigger_action)

    # 待機状態
    keyboard.wait()

if __name__ == "__main__":
    start_hotkey_service()
