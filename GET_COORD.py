import win32api
import win32con
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("====================================")
print("【師匠専属 座標スキャンシステム稼働！】")
print("====================================")
print("師匠、今からマウスの「左クリック」を監視します！")
print("目的のボタン（一番右より少し左）を普通にクリックしてください！")
print("クリックした瞬間の座標を自動的に記録し、Antigravity（私）に伝達します。")
print("（終了するにはこの黒い画面を閉じてください）\n")

log_file = r"C:\Users\yoshi\OneDrive\Desktop\StockProject\_target_coord.txt"

# 初期状態のクリック判定をクリアする
win32api.GetAsyncKeyState(win32con.VK_LBUTTON)

while True:
    state_left = win32api.GetAsyncKeyState(win32con.VK_LBUTTON)
    
    # 状態がゼロより小さい場合は現在押されている
    if state_left < 0:
        x, y = win32api.GetCursorPos()
        print(f"!!! クリック検知 !!!  座標: X={x}, Y={y}")
        
        # 記録用ファイルに書き出し
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"{x},{y}\n")
            
        # 連続記録を防ぐためのクールダウン
        time.sleep(0.5)
        
    time.sleep(0.01)
