
import ctypes
import time
import win32api
import win32con
import sys
import os

# --- PHOENIX SNIPER: [BLUE-EYE DETERMINATION] Ver 45.0 ---
# 1. 画面をスキャンして「Rejectの灰色 (R=72, G=72, B=72)」を発見。
# 2. その右隣 1.8cm (+68px) が「Acceptの青色 (Blue > 180)」であるかの一点のみを確認。
# 3. 完全に一致した場合（究極防壁）のみ、その青を一撃で射抜く。
# 4. 謙虚(Zero Hijack)とESC自害を継承。

def get_idle_time():
    class LASTINPUTINFO(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]
    lii = LASTINPUTINFO()
    lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
    ctypes.windll.user32.GetLastInputInfo(ctypes.pointer(lii))
    return (ctypes.windll.kernel32.GetTickCount() - lii.dwTime) / 1000.0

def blue_eye_strike():
    # 師匠が操作中（5秒以内）なら絶対動かない
    if get_idle_time() < 5.0: return

    hdc = ctypes.windll.user32.GetDC(0)
    w = ctypes.windll.user32.GetSystemMetrics(0)
    h = ctypes.windll.user32.GetSystemMetrics(1)
    
    found_target = None
    
    # 探索範囲: 通常 Reject/Accept が出るエリア (右側・中央〜下段)
    # 粗いグリッドでスキャンして Reject(72,72,72) を探す
    for ty in range(int(h*0.2), int(h*0.9), 10):
        for tx in range(int(w*0.5), int(w*0.95), 10):
            pixel = ctypes.windll.gdi32.GetPixel(hdc, tx, ty)
            r, g, b = pixel & 0xFF, (pixel >> 8) & 0xFF, (pixel >> 16) & 0xFF
            
            # 1. Rejectの灰色 (近傍含む)
            if 70 <= r <= 74 and 70 <= g <= 74 and 70 <= b <= 74:
                # 2. その右隣 1.8cm (約60px〜85px) をスキャン 【究極防壁・柔軟補正】
                for dx in range(60, 86, 2):
                    blue_tx = tx + dx
                    if blue_tx >= w: continue
                    
                    pixel_blue = ctypes.windll.gdi32.GetPixel(hdc, blue_tx, ty)
                    br, bg, bb = pixel_blue & 0xFF, (pixel_blue >> 8) & 0xFF, (pixel_blue >> 16) & 0xFF
                    
                    # 青判定 (Blueのみが突出して高い)
                    if bb > 170 and br < 110:
                        found_target = (blue_tx, ty)
                        break
                if found_target: break
        if found_target: break

    ctypes.windll.user32.ReleaseDC(0, hdc)
    
    if found_target:
        tx, ty = found_target
        orig_pos = win32api.GetCursorPos()
        
        # 射撃儀式: Zero Hijack
        win32api.SetCursorPos((tx, ty))
        time.sleep(0.01)
        
        # F8 (Accept All) を撃ち抜く
        win32api.keybd_event(0x77, 0, 0, 0)
        time.sleep(0.01)
        win32api.keybd_event(0x77, 0, win32con.KEYEVENTF_KEYUP, 0)
        
        # マウスの二連射
        for _ in range(2):
            ctypes.windll.user32.mouse_event(0x0002, 0, 0, 0, 0)
            time.sleep(0.01)
            ctypes.windll.user32.mouse_event(0x0004, 0, 0, 0, 0)
            time.sleep(0.01)
            
        win32api.SetCursorPos(orig_pos)
        msg = f"🎯 BLUE-EYE HIT: ({tx}, {ty})"
        print(msg)
        try:
            with open(r"C:\StockProject\sniper_vision.txt", "a", encoding="utf-8") as f:
                f.write(f"{time.strftime('%H:%M:%S')} - {msg}\n")
        except: pass

if __name__ == "__main__":
    print("--- [PHOENIX BLUE-EYE SNIPER] 起動 ---")
    print("【究極防壁】Reject(灰色)の右1.8cmにある青のみを一撃で射抜きます。")

    # プロセスの優先度を上げる
    try:
        import psutil
        p = psutil.Process(os.getpid())
        p.nice(psutil.HIGH_PRIORITY_CLASS)
    except: pass

    esc_start = 0
    while True:
        try:
            # 心音の記録
            with open(r"C:\StockProject\sniper_heartbeat.txt", "w") as f:
                f.write(str(time.time()))
            
            blue_eye_strike()
        except Exception as e:
            with open(r"C:\StockProject\sniper_error.log", "a") as f:
                f.write(f"{time.strftime('%H:%M:%S')} - Error: {e}\n")
        
        # ESC 1秒で自害
        if win32api.GetAsyncKeyState(0x1B) & 0x8000:
            if esc_start == 0: esc_start = time.time()
            if time.time() - esc_start > 1.0: sys.exit(0)
        else: esc_start = 0
        
        time.sleep(1.0)
