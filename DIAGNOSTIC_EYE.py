
import ctypes
import win32api

def diagnostic_eye():
    print("--- PHOENIX EYE: 視覚スキャン診断開始 ---")
    base_x, base_y = 1249, 531
    found_target = None
    
    hdc = ctypes.windll.user32.GetDC(0)
    print(f"スキャン開始位置: ({base_x}, {base_y}) 周辺")
    
    hits = 0
    sample_pixels = []
    
    for dy in range(-100, 100, 4):
        for dx in range(-200, 100, 4):
            tx, ty = base_x + dx, base_y + dy
            pixel = ctypes.windll.gdi32.GetPixel(hdc, tx, ty)
            r = pixel & 0xFF
            g = (pixel >> 8) & 0xFF
            b = (pixel >> 16) & 0xFF
            
            # スナイパーの実装と同じ判定基準
            if r < 100 and g > 80 and b > 160:
                if not found_target:
                    found_target = (tx, ty)
                hits += 1
            
            # 中央付近のピクセル情報をサンプルとして保持
            if abs(dx) < 10 and abs(dy) < 10:
                sample_pixels.append(((tx, ty), (r, g, b)))
                
    ctypes.windll.user32.ReleaseDC(0, hdc)
    
    if found_target:
        print(f"✅ 【標的捕捉】({found_target[0]}, {found_target[1]}) に青色ボタンの反応を確認！")
        print(f"総検知ピクセル数: {hits}")
    else:
        print("❌ 【未検知】青色ボタンを視認できませんでした。")
        print("スキャン中心付近のピクセルデータサンプル:")
        for pos, color in sample_pixels[:3]:
            print(f"  位置{pos}: RGB{color}")

if __name__ == "__main__":
    diagnostic_eye()
