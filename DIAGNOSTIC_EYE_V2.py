
import ctypes
import sys
import os

def diagnostic_eye():
    log_path = r"c:\Users\yoshi\OneDrive\Weekly report\Phoenix_Protocol\EYE_RESULT.txt"
    def log(msg):
        print(msg)
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(msg + "\n")
        sys.stdout.flush()

    if os.path.exists(log_path): os.remove(log_path)
    
    log("--- PHOENIX VISION DIAGNOSTIC Ver 2.0 ---")
    log("スキャンプロトコル開始...")

    base_x, base_y = 1249, 531
    found_target = None
    
    try:
        hdc = ctypes.windll.user32.GetDC(0)
        log(f"OSからの描画権限(HDC)取得成功。")
        
        target_blue_count = 0
        for dy in range(-150, 150, 5):
            for dx in range(-250, 150, 5):
                tx, ty = base_x + dx, base_y + dy
                pixel = ctypes.windll.gdi32.GetPixel(hdc, tx, ty)
                r = pixel & 0xFF
                g = (pixel >> 8) & 0xFF
                b = (pixel >> 16) & 0xFF
                
                # 判定: 青が強く、赤が少ない領域
                if r < 120 and g > 60 and b > 140:
                    if not found_target:
                        found_target = (tx, ty)
                    target_blue_count += 1
        
        ctypes.windll.user32.ReleaseDC(0, hdc)
        
        if found_target:
            log(f"✅ 【標的捕捉】({found_target[0]}, {found_target[1]}) に青色反応を検知！")
            log(f"検知ボリューム: {target_blue_count} ピクセル")
        else:
            log("❌ 【未検知】画面内に『師匠の青』が見つかりませんでした。")
            log("※ Alt+Enterボタンが他の窓に隠れていないか、または座標が大きく外れていないか確認してください。")

    except Exception as e:
        log(f"🔥 エラー発生: {str(e)}")

if __name__ == "__main__":
    diagnostic_eye()
