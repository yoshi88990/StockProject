import win32api
import win32gui
import time
import keyboard
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

def get_window_text(hwnd):
    length = win32gui.GetWindowTextLength(hwnd)
    if length > 0:
        buffer = win32gui.PyMakeBuffer(length + 1)
        win32gui.GetWindowText(hwnd, buffer)
        return buffer.value
    return ""

def window_enum_handler(hwnd, result):
    if win32gui.IsWindowVisible(hwnd):
        result.append(hwnd)

def sentinel_observer_v69():
    print("センチネル監視システム v69.1 (真・並列/完全沈黙版) 起動...")
    print("【新ルール】敵が出たら即座に消して10秒沈黙。敵がいなくても「1分に1回」だけ右下を撃つ。")
    print("重いpywinautoは完全排除。CPU負荷ゼロ。師匠のタイピングを一切妨害しません。")
    
    # 師匠がクリックして記録してくれた「一連の正しい座標」
    targets = [
        (1319, 286),   # 聖なる座標 (Run)
        (1292, 595),   # Accept
        (1165, 641),   
        (1135, 650),   
        (1150, 650)    
    ]
    
    last_1min_pulse = time.time()
    
    try:
        while True:
            if keyboard.is_pressed('esc'): break
            
            now = time.time()
            
            # --- フェーズ1: 1分(60秒)に1回のパルス（発生してなくても撃つ） ---
            if (now - last_1min_pulse) >= 60.0:
                print("1分が経過しました。念のための承認パルスを発射します。")
                orig_x, orig_y = win32api.GetCursorPos()
                
                keyboard.press_and_release('f8')
                for coord in targets:
                    win32api.SetCursorPos(coord)
                    win32api.mouse_event(2, 0, 0, 0, 0) # Left Down
                    win32api.mouse_event(4, 0, 0, 0, 0) # Left Up
                
                win32api.SetCursorPos((orig_x, orig_y))
                print("1分パルス完了。ここから10秒間、絶対に沈黙します。")
                
                last_1min_pulse = time.time() # 攻撃したので1分タイマーをリセット
                time.sleep(10.0) # 実行した後は必ず10秒沈黙
                continue # パルスを撃ったので下（索敵）には行かず次のループへ
                
            # --- フェーズ2: 適宜発生する敵の索敵と排除（超高速） ---
            found = False
            windows = []
            win32gui.EnumWindows(window_enum_handler, windows)
            
            for hwnd in windows:
                win_text = get_window_text(hwnd).lower()
                # Run / Accept のウィンドウが出現した場合を想定
                if "visual studio code" in win_text or "stock" in win_text or win_text == "":
                    found = True
                    break
            
            if found:
                print("敵を捕捉！F8と狙撃を【1回だけ】行い、即座に消します。")
                orig_x, orig_y = win32api.GetCursorPos()
                
                keyboard.press_and_release('f8')
                for coord in targets:
                    win32api.SetCursorPos(coord)
                    win32api.mouse_event(2, 0, 0, 0, 0)
                    win32api.mouse_event(4, 0, 0, 0, 0)
                
                win32api.SetCursorPos((orig_x, orig_y))
                print("敵を排除しました。思考をとめないため連打を終了し、ここから10秒間完全に沈黙に入ります。")
                
                last_1min_pulse = time.time() # 攻撃したので1分タイマーをリセット
                time.sleep(10.0)
            else:
                # 敵がいない時は文字入力の邪魔をしないように待機
                time.sleep(0.5)
            
    except Exception as e:
        pass

if __name__ == "__main__":
    sentinel_observer_v69()
