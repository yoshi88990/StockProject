
import pyautogui
import time
from PIL import Image

def scan_for_blue_button():
    print("--- PHOENIX EYE: 色覚調整プロトコル開始 ---")
    print("5秒以内に、AIチャットの『Alt+Enter』ボタンを見える位置に出してください...")
    time.sleep(5)
    
    screenshot = pyautogui.screenshot()
    width, height = screenshot.size
    
    # Cursor/VSCodeの一般的な青色ボタンの色の範囲 (R, G, B)
    # 通常の青: (0, 122, 204) や (5, 117, 197) あたり
    target_blue_min = (0, 100, 180)
    target_blue_max = (100, 160, 255)
    
    found_points = []
    
    # 処理高速化のため、画面の右半分（チャット欄がある側）を重点スキャン
    # 師匠の命により、画面上端 60px (約1.5cm) は自爆防止のためスキャン対象外とする
    for x in range(int(width * 0.5), width, 5):
        for y in range(60, height, 5):
            r, g, b = screenshot.getpixel((x, y))
            if target_blue_min[0] <= r <= target_blue_max[0] and \
               target_blue_min[1] <= g <= target_blue_max[1] and \
               target_blue_min[2] <= b <= target_blue_max[2]:
                found_points.append((x, y))
    
    if found_points:
        # 重心を計算して、ボタンの中央を特定
        avg_x = sum(p[0] for p in found_points) // len(found_points)
        avg_y = sum(p[1] for p in found_points) // len(found_points)
        print(f"【標的捕捉】青色ボタンの反応を確認: ({avg_x}, {avg_y})")
        print(f"ピクセル色: {screenshot.getpixel((avg_x, avg_y))}")
        return avg_x, avg_y
    else:
        print("【失敗】青色ボタンが見つかりませんでした。")
        return None

if __name__ == "__main__":
    scan_for_blue_button()
