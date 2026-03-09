
import ctypes
import time
import win32api
import win32con
import win32gui
import sys
import os

# --- PHOENIX SNIPER: [BLUE-BOLT RESONANCE] Ver 42.0 ---
# 師匠の命：最新をスキャンしてから打ち抜く。
# 1. 画面全体の「Accept青 (R<100, B>180)」を高速スキャン。
# 2. 座標を特定し、一撃で射抜く。
# 3. 謙虚(Zero Hijack)とESC自害を継承。

def get_idle_time():
    class LASTINPUTINFO(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]
    lii = LASTINPUTINFO()
    lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
    ctypes.windll.user32.GetLastInputInfo(ctypes.pointer(lii))
    return (ctypes.windll.kernel32.GetTickCount() - lii.dwTime) / 1000.0

def scan_and_strike():
    # 師匠が操作中なら絶対動かない
    if get_idle_time() < 5.0: return

    hdc = ctypes.windll.user32.GetDC(0)
    w = ctypes.windll.user32.GetSystemMetrics(0)
    h = ctypes.windll.user32.GetSystemMetrics(1)
    
    # 探索エリアの絞り込み（右下周辺を優先）
    # 通常、Acceptボタンが出るのは右側中段〜下段
    found_target = None
    
    # 高速スキャン (粗め)
    for ty in range(int(h*0.2), int(h*0.9), 20):
        for tx in range(int(w*0.5), int(w*0.95), 25):
            pixel = ctypes.windll.gdi32.GetPixel(hdc, tx, ty)
            r, g, b = pixel & 0xFF, (pixel >> 8) & 0xFF, (pixel >> 16) & 0xFF
            
            # 精密な青判定 (Acceptボタンの青)
            if b > 200 and r < 80 and g < 180:
                # 付近を再スキャンして「ボタンらしい塊」か確認
                confirm_count = 0
                for sy in range(-5, 6, 5):
                    for sx in range(-10, 11, 10):
                        px2 = ctypes.windll.gdi32.GetPixel(hdc, tx+sx, ty+sy)
                        if (px2 >> 16) & 0xFF > 180: confirm_count += 1
                
                if confirm_count >= 3:
                    found_target = (tx, ty)
                    break
        if found_target: break

    ctypes.windll.user32.ReleaseDC(0, hdc)
    
    if found_target:
        tx, ty = found_target
        orig_pos = win32api.GetCursorPos()
        
        # 射撃儀式
        win32api.SetCursorPos((tx, ty))
        time.sleep(0.02)
        
        # F8 (Accept All) を物理的にシミュレート
        win32api.keybd_event(0x77, 0, 0, 0)
        time.sleep(0.01)
        win32api.keybd_event(0x77, 0, win32con.KEYEVENTF_KEYUP, 0)
        
        # マウスクリック二連
        for _ in range(2):
            ctypes.windll.user32.mouse_event(0x0002, 0, 0, 0, 0)
            time.sleep(0.01)
            ctypes.windll.user32.mouse_event(0x0004, 0, 0, 0, 0)
            time.sleep(0.01)
            
        win32api.SetCursorPos(orig_pos)
        print(f"🔥 SCAN-HIT: ({tx}, {ty})")

if __name__ == "__main__":
    print("--- [PHOENIX BLUE-BOLT] 起動 ---")
    print("最新をスキャンして打ち抜きます。")
    esc_start = 0
    while True:
        scan_and_strike()
        
        # ESC 1秒で自害
        if win32api.GetAsyncKeyState(0x1B) & 0x8000:
            if esc_start == 0: esc_start = time.time()
            if time.time() - esc_start > 1.0: sys.exit(0)
        else: esc_start = 0
        
        time.sleep(1.0) # スキャン周期
