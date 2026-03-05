import ctypes
import time
import win32api
import win32con
import win32gui
import sys
import os

# --- 極小メモリ・24時間稼働 AcceptAll エンジン (v5.3-ZeroHijack-Core) ---
# 師匠の命により、「文字入力中は完全に静止」し、
# 「エンターキー押下3秒後」にのみ狙撃を再開する究極の安全モデル。
# マウス権限を絶対に奪わない（師匠の操作優先）。

# --- Win32/Ctypes Setup ---
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort), ("wScan", ctypes.c_ushort), ("dwFlags", ctypes.c_ulong), ("time", ctypes.c_ulong), ("dwExtraInfo", PUL)]
class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput)]
class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong), ("ii", Input_I)]

class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_ulong)]

VK_F8 = 0x77
SCAN_F8 = 0x42
KEYEVENTF_SCANCODE = 0x0008
KEYEVENTF_KEYUP = 0x0002

ACCEPT_ALL_TARGETS = [
    (1292, 600), (1319, 286), (1292, 595), (1165, 641), (1135, 650), (1150, 650)
]

def get_idle_time():
    """OSから最後の入力からの経過時間を取得"""
    lii = LASTINPUTINFO()
    lii.cbSize = ctypes.sizeof(lii)
    ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii))
    millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
    return millis / 1000.0

def is_typing_activity():
    """師匠が文字を打鍵中かどうかを検知（マウス権限保護用）"""
    # 0x08 (BackSpace) から 0x90 (NumLock) までの主要キーをスキャン
    for i in range(0x08, 0x91):
        if win32api.GetAsyncKeyState(i) & 0x8001:
            return True
    return False

def fire_omni_f8():
    user32 = ctypes.windll.user32
    try:
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.ki = KeyBdInput(0, SCAN_F8, KEYEVENTF_SCANCODE, 0, ctypes.pointer(extra))
        x = Input(ctypes.c_ulong(1), ii_)
        user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
        time.sleep(0.01)
        ii_.ki = KeyBdInput(0, SCAN_F8, KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP, 0, ctypes.pointer(extra))
        x = Input(ctypes.c_ulong(1), ii_)
        user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
    except: pass

def execute_accept_all():
    """精密狙撃 (マウス権限死守・文字入力優先版)"""
    try:
        # 1. 文字入力中の検知（執筆中は絶対にマウスを動かさない）
        if is_typing_activity():
            return

        # 2. エンターキー押下をトリガーにする
        # GetAsyncKeyState(0x0D) & 0x8001 -> 「今押されている」または「前回の呼び出し以降に押された」
        is_enter_pressed = win32api.GetAsyncKeyState(0x0D) & 0x8001
        
        idle_time = get_idle_time()

        # 判定：師匠がエンターを押した3秒後、または15秒以上の完全な静寂がある場合のみ
        if is_enter_pressed:
            time.sleep(3.0) # 3秒の余韻
            # 3秒待機中に再度入力があったら中止
            if get_idle_time() < 1.0: return
        elif idle_time < 15.0:
            return

        # 狙撃実行（マウス移動＆クリック）
        fire_omni_f8()
        orig_pos = win32api.GetCursorPos()
        for tx, ty in ACCEPT_ALL_TARGETS:
            # 実行直前にもう一度アイドルチェック（マウスを勝手に動かさない究極の誓い）
            if get_idle_time() < 0.5: break
            win32api.SetCursorPos((tx, ty))
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            time.sleep(0.005) 
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            time.sleep(0.01)
        win32api.SetCursorPos(orig_pos)

        # 「Review Changes」ウィンドウを閉じる (Ctrl+W)
        hwnd = win32gui.GetForegroundWindow()
        if hwnd:
            window_title = win32gui.GetWindowText(hwnd)
            if "Review Changes" in window_title:
                win32api.keybd_event(0x11, 0, 0, 0) # Ctrl
                win32api.keybd_event(0x57, 0, 0, 0) # W
                time.sleep(0.02)
                win32api.keybd_event(0x57, 0, win32con.KEYEVENTF_KEYUP, 0)
                win32api.keybd_event(0x11, 0, win32con.KEYEVENTF_KEYUP, 0)
    except Exception:
        pass

if __name__ == "__main__":
    # OS優先度を ABOVE_NORMAL に設定
    try:
        kernel32 = ctypes.windll.kernel32
        process = kernel32.GetCurrentProcess()
        kernel32.SetPriorityClass(process, 0x00008000)
    except: pass

    HB_FILE = r"C:\Phoenix_Core\sniper_heartbeat.txt"
    while True:
        try:
            with open(HB_FILE, "w") as f:
                f.write(str(time.time()))
        except: pass

        execute_accept_all()
        time.sleep(30.0)
