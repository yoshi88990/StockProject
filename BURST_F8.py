import ctypes
import time

# 物理スキャンコード 定義
SCAN_F8 = 0x42
KEYEVENTF_SCANCODE = 0x0008
KEYEVENTF_KEYUP = 0x0002

# win32 構造体 定義
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]
class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput)]
class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

def press_f8_burst(count=5):
    print(f"!!! 物理打鍵プロトコル：{count}連射開始 (F8) !!!")
    extra = ctypes.c_ulong(0)
    
    for i in range(count):
        # Press
        ii_ = Input_I()
        ii_.ki = KeyBdInput(0, SCAN_F8, KEYEVENTF_SCANCODE, 0, ctypes.pointer(extra))
        x = Input(ctypes.c_ulong(1), ii_)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

        time.sleep(0.05)

        # Release
        ii_.ki = KeyBdInput(0, SCAN_F8, KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP, 0, ctypes.pointer(extra))
        x = Input(ctypes.c_ulong(1), ii_)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
        
        print(f"[{i+1}] Key F8 Shot")
        time.sleep(0.5)

if __name__ == "__main__":
    press_f8_burst(5)
