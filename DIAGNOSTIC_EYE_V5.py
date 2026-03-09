
import ctypes
import sys
import time

def high_speed_sync():
    log_path = r"c:\Users\yoshi\OneDrive\Weekly report\Phoenix_Protocol\EYE_RESULT.txt"
    def log(msg):
        print(msg)
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(msg + "\n")
        sys.stdout.flush()

    log("--- PHOENIX REALTIME-VISION Ver 5.0 ---")
    
    # 前回の有力候補: (1159, 361)
    targets = [(1159, 361), (1249, 531), (1000, 400), (1300, 600)]
    
    hdc = ctypes.windll.user32.GetDC(0)
    log("コア・スキャン開始...")
    
    found = False
    for i, (bx, by) in enumerate(targets):
        log(f"エリア {i+1} 索敵中: 中心({bx}, {by})")
        for dy in range(-100, 100, 20):
            for dx in range(-100, 100, 20):
                tx, ty = bx + dx, by + dy
                pixel = ctypes.windll.gdi32.GetPixel(hdc, tx, ty)
                r, g, b = pixel & 0xFF, (pixel >> 8) & 0xFF, (pixel >> 16) & 0xFF
                
                if b > 140 and r < 120:
                    log(f"🔥 反応あり! ({tx}, {ty}) RGB({r},{g},{b})")
                    found = True
                    break
            if found: break
        if found: break
    
    ctypes.windll.user32.ReleaseDC(0, hdc)
    if not found:
        log("全エリアで決定的な青を検知できませんでした。環境光設定を確認します。")

if __name__ == "__main__":
    high_speed_sync()
