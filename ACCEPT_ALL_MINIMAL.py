import ctypes
import time
import win32api
import win32con
import win32gui
import sys
import os
import mss
import numpy as np

# ==============================================================================
# 【PHOENIX SNIPER: TRUE FLUID DNA】 Ver 50.3
# 
# 1. Reject(灰色)を索敵し、その 1.8cm(+68px)右の Accept(青色)を貫く。
# 2. 画面上端 60px (1.5cm) は「絶対聖域」として狙撃を封印。
# 3. 5秒間のアイドル＋エディタ非活性時のみ動作。
# 4. マウス権限を奪わない Zero Hijack 座標復元型。
# ==============================================================================

# --- 設定：絶対聖域と座標定義 ---
SANCTUARY_Y = 60  # 画面上端 1.5cm 回避
REJECT_GRAY = [200, 200, 200]  # 標準的な灰色の閾値
ACCEPT_BLUE_OFFSET = 68        # Rejectから右へのオフセット (1.8cm)
ACCEPTALL_STRIKE_COORD = (1249, 531)  # 【不動の聖域】師匠指定の固定座標

class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]

def get_idle_time():
    lii = LASTINPUTINFO()
    lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
    ctypes.windll.user32.GetLastInputInfo(ctypes.pointer(lii))
    return (ctypes.windll.kernel32.GetTickCount() - lii.dwTime) / 1000.0

def log_vision(msg):
    try:
        with open(r"C:\StockProject\sniper_vision.txt", "a", encoding="utf-8") as f:
            f.write(f"[{time.strftime('%H:%M:%S')}] {msg}\n")
    except: pass

def is_user_operating(orig_pos):
    curr_pos = win32api.GetCursorPos()
    if abs(curr_pos[0] - orig_pos[0]) > 1 or abs(curr_pos[1] - orig_pos[1]) > 1:
        return True
    if get_idle_time() < 0.5:
        return True
    return False

def strike_ritual(tx, ty, label):
    if ty < SANCTUARY_Y:
        log_vision(f"SANCTUARY:({tx},{ty}) は聖域のため回避。")
        return
    
    try:
        orig_pos = win32api.GetCursorPos()
        if is_user_operating(orig_pos):
            log_vision(f"ABORT[{label}]: ご操作検知。")
            return

        win32api.SetCursorPos((tx, ty))
        time.sleep(0.01)

        # 師匠の二連射
        for _ in range(2):
            ctypes.windll.user32.mouse_event(0x0002, 0, 0, 0, 0)
            time.sleep(0.01)
            ctypes.windll.user32.mouse_event(0x0004, 0, 0, 0, 0)
            time.sleep(0.01)
            
        win32api.SetCursorPos(orig_pos)
        log_vision(f"HIT[{label}]: ({tx},{ty})")
    except Exception as e:
        log_vision(f"ERROR: {e}")

def fluid_scan_and_strike():
    """『真の眼』: スキャン後に標的が実在する場合のみ撃つ"""
    try:
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            img = np.array(sct.grab(monitor))
            
            # 灰色(Reject)を探す
            gray_mask = (img[:, :, 0] > 180) & (img[:, :, 1] > 180) & (img[:, :, 2] > 180) & \
                        (abs(img[:, :, 0].astype(int) - img[:, :, 1].astype(int)) < 10)
            
            scan_y_start = SANCTUARY_Y
            scan_x_start = int(monitor['width'] * 0.5)
            
            gray_indices = np.where(gray_mask[scan_y_start:, scan_x_start:])
            
            if len(gray_indices[0]) > 0:
                y, x = gray_indices[0][0] + scan_y_start, gray_indices[1][0] + scan_x_start
                target_x = x + ACCEPT_BLUE_OFFSET
                
                if target_x < monitor['width']:
                    pixel = img[y, target_x]
                    if pixel[0] > 180 and pixel[2] < 120:
                        log_vision(f"FLUID TARGET DETECTED: ({target_x},{y})")
                        strike_ritual(target_x, y, "FLUID_SCAN")
                        return True
    except Exception as e:
        log_vision(f"SCAN ERROR: {e}")
    return False

def check_vscode_foreground():
    hwnd = win32gui.GetForegroundWindow()
    if hwnd:
        title = win32gui.GetWindowText(hwnd)
        if "Visual Studio Code" in title or "Cursor" in title:
            return True
    return False

if __name__ == "__main__":
    try: ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x00000020)
    except: pass

    last_fixed_strike_time = 0
    last_alive_log = 0
    log_vision("--- PHOENIX SNIPER GO ---")

    while True:
        try:
            now = time.time()
            with open(r"C:\StockProject\sniper_heartbeat.txt", "w") as f: f.write(str(now))
            
            # 生存ログ
            if now - last_alive_log >= 300.0:
                log_vision("SYSTEM ALIVE: 標的を監視中...")
                last_alive_log = now

            # フェーズ1: 流動索敵
            if get_idle_time() >= 5.0 and not check_vscode_foreground():
                fluid_scan_and_strike()
                
            # フェーズ2: 固定座標狙撃
            if now - last_fixed_strike_time >= 60.0:
                if get_idle_time() >= 3.0: 
                    strike_ritual(ACCEPTALL_STRIKE_COORD[0], ACCEPTALL_STRIKE_COORD[1], "acceptall_FIXED")
                    last_fixed_strike_time = now
                
            if win32api.GetAsyncKeyState(0x1B) & 0x8000:
                time.sleep(1.0)
                if win32api.GetAsyncKeyState(0x1B) & 0x8000: sys.exit(0)
                
        except Exception as e:
            log_vision(f"LOOP ERROR: {e}")
        time.sleep(1.0)
