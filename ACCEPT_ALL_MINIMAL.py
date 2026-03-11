# -*- coding: utf-8 -*-
import ctypes
import time
import win32api
import win32con
import win32gui
import sys
import os

# ==============================================================================
# 【PHOENIX MECHANICAL SNIPER】 Ver 60.0 - 亡霊根絶版 (DNA_VAULT 同期)
# 
# 1. 師匠指定の固定座標 (1249, 531) のみを見守る。
# 2. 余計なスキャン・索敵は一切行わない。
# 3. 5秒間の完全アイドル時のみ動作。
# 4. STOP_PHOENIX 信号検知時は即座に停止。
# ==============================================================================

# --- 設定：絶対座標と信号 ---
PROTOCOL_DIR = r"P:/"
STOP_SIGNAL = os.path.join(PROTOCOL_DIR, "STOP_PHOENIX")
FIXED_TARGET = (1249, 531)  # 【不動の聖域】師匠指定
HEARTBEAT_FILE = os.path.join(PROTOCOL_DIR, "PHOENIX_HEARTBEATS", "hb_Mechanical.txt")

class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]

def get_idle_time():
    lii = LASTINPUTINFO()
    lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
    ctypes.windll.user32.GetLastInputInfo(ctypes.pointer(lii))
    return (ctypes.windll.kernel32.GetTickCount() - lii.dwTime) / 1000.0

def strike_mechanical():
    """機械的な二連射：座標復元型"""
    try:
        orig_pos = win32api.GetCursorPos()
        # 操作検知(遊び)
        time.sleep(0.01)
        if get_idle_time() < 1.0: return

        win32api.SetCursorPos(FIXED_TARGET)
        time.sleep(0.02)
        
        # 師匠の二連射
        for _ in range(2):
            ctypes.windll.user32.mouse_event(0x0002, 0, 0, 0, 0)
            time.sleep(0.01)
            ctypes.windll.user32.mouse_event(0x0004, 0, 0, 0, 0)
            time.sleep(0.01)
            
        win32api.SetCursorPos(orig_pos)
    except: pass

def check_vscode_foreground():
    hwnd = win32gui.GetForegroundWindow()
    if hwnd:
        title = win32gui.GetWindowText(hwnd)
        # Antigravity（私）や VS Code が前面にいる時は「思考中」とみなす
        if "Visual Studio Code" in title or "Cursor" in title or "Antigravity" in title:
            return True
    return False

if __name__ == "__main__":
    # プロセス優先度を下げてPCの負荷を最小化
    try: ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x00000020)
    except: pass

    last_strike = 0
    
    while True:
        try:
            # 停止信号チェック
            if os.path.exists(STOP_SIGNAL):
                time.sleep(5)
                continue

            now = time.time()
            # 師匠の命：心拍(Heartbeat)を刻む
            hb_dir = os.path.dirname(HEARTBEAT_FILE)
            if not os.path.exists(hb_dir):
                os.makedirs(hb_dir, exist_ok=True)
            with open(HEARTBEAT_FILE, "w") as f: f.write(str(now))
            
            # 【後醍醐プロトコル】：5秒間の静寂を検知したら即座に点火
            if get_idle_time() >= 5.0 and not check_vscode_foreground():
                # 5秒おきに連射し、停滞を許さない
                if now - last_strike >= 5.0:
                    strike_mechanical()
                    last_strike = now
                    
            if win32api.GetAsyncKeyState(0x1B) & 0x8000: sys.exit(0) # ESCで緊急停止
                
        except Exception:
            time.sleep(1.0)
        time.sleep(1.0)
