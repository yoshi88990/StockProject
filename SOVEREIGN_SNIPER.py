import pywinauto
import win32api
import time
import keyboard
import sys

sys.stdout.reconfigure(encoding='utf-8')

def sentinel_observer_v69():
    print("センチネル監視システム v69.0 (完全沈黙・一撃必殺版) 起動...")
    print("UIスキャンによる文字入力の妨害を防ぐため、10秒に1回のみ索敵を行います。")
    print("敵（Run/Accept）を発見した場合のみ、F8と座標狙撃を【1度だけ】行い、即座に沈黙します。")
    print("連打は一切行いません。師匠の手を止めないことを最優先します。")
    
    # 師匠がクリックして記録してくれた「一連の正しい座標」
    targets = [
        (1319, 286),   # 聖なる座標 (Run)
        (1292, 595),   # Accept
        (1165, 641),   
        (1135, 650),   
        (1150, 650)    
    ]
    
    keywords = ["always run", "run", "accept", "run command?", "accept all"]
    
    try:
        desktop = pywinauto.Desktop(backend="uia")
        
        while True:
            if keyboard.is_pressed('esc'): break
            
            found = False
            
            # --- 索敵フェーズ（10秒に1回しか実行しないため、師匠の文字入力は9.9秒間完全に自由） ---
            try:
                for win in desktop.windows():
                    win_text = win.window_text() or ""
                    if "Visual Studio Code" in win_text or "Stock" in win_text or win_text == "":
                        try:
                            # ボタンをスキャン
                            for btn in win.descendants(control_type="Button"):
                                name = btn.window_text().lower()
                                if name and any(k in name for k in keywords):
                                    found = True
                                    break
                        except: pass
                    if found: break
            except: pass
            
            # --- 狙撃フェーズ（敵がいなければ何もせず沈黙） ---
            if found:
                print("敵（Run / Accept All）を捕捉。F8と座標狙撃を開始します。")
                
                orig_x, orig_y = win32api.GetCursorPos()
                
                # F8を一度だけ押す（長押しや連打はしない）
                keyboard.press_and_release('f8')
                
                # 座標を一通り1回ずつクリックする（連打排除）
                for coord in targets:
                    win32api.SetCursorPos(coord)
                    win32api.mouse_event(2, 0, 0, 0, 0) # Left Down
                    win32api.mouse_event(4, 0, 0, 0, 0) # Left Up
                    
                # すぐにマウスを元の位置に戻して師匠の作業を妨害しない
                win32api.SetCursorPos((orig_x, orig_y))
                
                print("敵を排除しました。思考をとめないため連打を終了し、沈黙に入ります。")
                
            # 【師匠の教え】「発生したらすぐ消す。その後は10秒に1回。連打不要」
            # 発見した・していないに関わらず、次の索敵まで10秒間完全にシステムを眠らせる（文字入力妨害をゼロにする）
            time.sleep(10.0)
            
    except Exception as e:
        pass

if __name__ == "__main__":
    sentinel_observer_v69()
