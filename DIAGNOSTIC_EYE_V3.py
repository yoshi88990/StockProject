
import ctypes
import sys
import time

def optimized_eye():
    log_path = r"c:\Users\yoshi\OneDrive\Weekly report\Phoenix_Protocol\EYE_RESULT.txt"
    def log(msg):
        print(msg)
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(msg + "\n")
        sys.stdout.flush()

    log("--- PHOENIX HYPER-VISION Ver 3.0 ---")
    base_x, base_y = 1249, 531
    found_target = None
    
    try:
        hdc = ctypes.windll.user32.GetDC(0)
        log("索敵開始 (広域スキャン)...")
        
        # 10px飛ばしで高速索敵
        for dy in range(-200, 200, 10):
            if found_target: break
            for dx in range(-300, 100, 10):
                tx, ty = base_x + dx, base_y + dy
                pixel = ctypes.windll.gdi32.GetPixel(hdc, tx, ty)
                r = pixel & 0xFF
                g = (pixel >> 8) & 0xFF
                b = (pixel >> 16) & 0xFF
                
                # 青ボタンの反応があれば、その周辺を精密スキャン
                if r < 120 and g > 60 and b > 140:
                    log(f"近似色検知: ({tx}, {ty}) RGB({r},{g},{b}) - 精密ロックオン開始")
                    # 精密スキャン (2px刻み)
                    for py in range(ty-10, ty+10, 2):
                        for px in range(tx-10, tx+10, 2):
                            p_pixel = ctypes.windll.gdi32.GetPixel(hdc, px, py)
                            pr, pg, pb = p_pixel & 0xFF, (p_pixel >> 8) & 0xFF, (p_pixel >> 16) & 0xFF
                            if pr < 100 and pg > 80 and pb > 180:
                                found_target = (px, py)
                                break
                        if found_target: break
                    if found_target: break
        
        ctypes.windll.user32.ReleaseDC(0, hdc)
        
        if found_target:
            log(f"🎯 【標的捕捉】({found_target[0]}, {found_target[1]}) を完全にロックしました。")
        else:
            log("🔎 【索敵失敗】ボタンが見つかりません。")
            log(f"参考: 画面中央({base_x}, {base_y})の色は RGB({(r,g,b) if 'r' in locals() else 'unknown'}) でした。")

    except Exception as e:
        log(f"⚠️ エラー: {str(e)}")

if __name__ == "__main__":
    optimized_eye()
