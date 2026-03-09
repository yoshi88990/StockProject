
import ctypes
import sys
import os

def adaptive_vision():
    log_path = r"c:\Users\yoshi\OneDrive\Weekly report\Phoenix_Protocol\EYE_RESULT.txt"
    def log(msg):
        print(msg)
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(msg + "\n")
        sys.stdout.flush()

    log("--- PHOENIX ADAPTIVE-VISION Ver 4.0 ---")
    base_x, base_y = 1249, 531
    best_target = None
    best_blue_score = -1000
    
    try:
        hdc = ctypes.windll.user32.GetDC(0)
        log("全方位・最強色覚スキャン開始...")
        
        # 12px刻みで高速全域スキャン (約1000点)
        for dy in range(-250, 250, 12):
            for dx in range(-400, 150, 12):
                tx, ty = base_x + dx, base_y + dy
                pixel = ctypes.windll.gdi32.GetPixel(hdc, tx, ty)
                r = pixel & 0xFF
                g = (pixel >> 8) & 0xFF
                b = (pixel >> 16) & 0xFF
                
                # 「青さスコア」を計算: 青が強く、赤が少ないほど高スコア
                score = b - r
                if score > best_blue_score:
                    best_blue_score = score
                    best_target = (tx, ty, r, g, b)
        
        ctypes.windll.user32.ReleaseDC(0, hdc)
        
        if best_target and best_blue_score > 50:
            tx, ty, tr, tg, tb = best_target
            log(f"🎯 【標的捕捉】最強の青を発見: ({tx}, {ty})")
            log(f"色情報: RGB({tr}, {tg}, {tb}) / 青さスコア: {best_blue_score}")
            log("この座標を『Alt+Enter』ボタンとしてロックオン可能です。")
        else:
            log("❌ 【捕捉失敗】十分な青色が検出されませんでした。")

    except Exception as e:
        log(f"⚠️ 致命的エラー: {str(e)}")

if __name__ == "__main__":
    adaptive_vision()
