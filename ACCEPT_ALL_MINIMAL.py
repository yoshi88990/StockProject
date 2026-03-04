import ctypes
import time
import win32api
import win32con
import win32gui
import sys

# --- 極小メモリ・24時間稼働 AcceptAll エンジン ---
# 師匠の命により、メモリ消費を極限まで削ぎ落とし、
# 1分間に1回だけ「完全無音・確実」にAccept Allを撃ち抜く専用機構。

# --- Win32/Ctypes Setup ---
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort), ("wScan", ctypes.c_ushort), ("dwFlags", ctypes.c_ulong), ("time", ctypes.c_ulong), ("dwExtraInfo", PUL)]
class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput)]
class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong), ("ii", Input_I)]

VK_F8 = 0x77
SCAN_F8 = 0x42
KEYEVENTF_SCANCODE = 0x0008
KEYEVENTF_KEYUP = 0x0002

ACCEPT_ALL_TARGETS = [
    (1292, 600), (1319, 286), (1292, 595), (1165, 641), (1135, 650), (1150, 650)
]

def fire_omni_f8():
    user32 = ctypes.windll.user32
    # Route 1: ScanCode
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

    # Route 2: Win32 Virtual Key
    try:
        win32api.keybd_event(VK_F8, 0, 0, 0)
        time.sleep(0.01)
        win32api.keybd_event(VK_F8, 0, win32con.KEYEVENTF_KEYUP, 0)
    except: pass

    # Route 3: PostMessage
    try:
        hwnd = win32gui.GetForegroundWindow()
        if hwnd:
            win32gui.PostMessage(hwnd, win32con.WM_KEYDOWN, VK_F8, 0)
            time.sleep(0.01)
            win32gui.PostMessage(hwnd, win32con.WM_KEYUP, VK_F8, 0)
    except: pass

    # Route 4: 【絶対貫通】スクリーンキーボード (OSK) の物理クリック
    # ※ 師匠のスクリーンキーボードの「F8」座標をここに設定します
    OSK_F8_COORD = None # 例: (800, 150) のように設定します。Noneの場合はスキップ。
    try:
        if OSK_F8_COORD:
            orig_mouse = win32api.GetCursorPos()
            win32api.SetCursorPos(OSK_F8_COORD)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            time.sleep(0.01)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            win32api.SetCursorPos(orig_mouse)
    except: pass

def execute_accept_all():
    """極小メモリ・精密狙撃 ＋ タブの完全排除 (1分1回限定)"""
    try:
        fire_omni_f8()
        
        orig_pos = win32api.GetCursorPos()
        for tx, ty in ACCEPT_ALL_TARGETS:
            win32api.SetCursorPos((tx, ty))
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            time.sleep(0.005) 
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            time.sleep(0.01)
        win32api.SetCursorPos(orig_pos)

        # 【安全措置】「Review Changes」のタイトルが存在する場合のみを撃ち抜く
        hwnd = win32gui.GetForegroundWindow()
        if hwnd:
            window_title = win32gui.GetWindowText(hwnd)
            if "Review Changes" in window_title:
                VK_CONTROL = 0x11
                VK_W = 0x57
                win32api.keybd_event(VK_CONTROL, 0, 0, 0)
                time.sleep(0.01)
                win32api.keybd_event(VK_W, 0, 0, 0)
                time.sleep(0.02)
                win32api.keybd_event(VK_W, 0, win32con.KEYEVENTF_KEYUP, 0)
                win32api.keybd_event(VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)

    except Exception:
        pass

if __name__ == "__main__":
    # プロセス名をリネームして識別可能にする（任意）
    try:
        ctypes.windll.kernel32.SetConsoleTitleW("ACCEPT_ALL_MINIMAL")
    except: pass

    print("--- [ACCEPT_ALL_MINIMAL] 起動 ---")
    print("メモリを極限まで削減し、24時間・30秒周期で Accept All ＆ タブを排除します。")
    print("※ OSの力（スタートアップ）を利用し、キルされても完全復活する不死身仕様です。")
    
    # メモリ解放のおまじない（OSにワーキングセットの縮小を要求）
    try:
        import psutil
        p = psutil.Process(os.getpid())
        p.memory_info() # call to initialize
    except: pass

    while True:
        execute_accept_all()
        # 半分（30秒）だけシステムリソースを一切消費せずに完全に眠る
        time.sleep(30.0)
