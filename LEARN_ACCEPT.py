import win32api
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

def simple_recorder_v66():
    print("【知能継承モード：Accept all 捕捉 (v66.0)】")
    print("合言葉『右下』を物理的に確認。クリック待機中...")
    
    log_file = "MASTER_WISDOM_COORDS_ACCEPT.txt"
    
    try:
        clicked = False
        while not clicked:
            # win32api.GetAsyncKeyState(0x01) を使用してクリックを拾う
            if win32api.GetAsyncKeyState(0x01) & 0x8000:
                # win32api.GetCursorPos() で正確な座標を拾う
                x, y = win32api.GetCursorPos()
                print(f"\n！！！ Accept all 座標を捕捉 ！！！: ({x}, {y})")
                
                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(f"{x},{y}\n")
                
                print(f"座標 ({x}, {y}) を記録完了。")
                clicked = True
            
            time.sleep(0.01)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    simple_recorder_v66()
