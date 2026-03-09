をimport ctypes
import time
import win32api
import win32con
import win32gui
import sys
import os

HB_FILE = r"C:\StockProject\sniper_heartbeat.txt"

def fire_omni_f8():
    user32 = ctypes.windll.user32
    # Route 1: ScanCode
    try:
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.ki = KeyBdInput(0, 0x42, 0x0008, 0, ctypes.pointer(extra))
        x = Input(ctypes.c_ulong(1), ii_)
        user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
        time.sleep(0.01)
        ii_.ki = KeyBdInput(0, 0x42, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
        x = Input(ctypes.c_ulong(1), ii_)
        user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
    except: pass

class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort), ("wScan", ctypes.c_ushort), ("dwFlags", ctypes.c_ulong), ("time", ctypes.c_ulong), ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]
class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput)]
class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong), ("ii", Input_I)]

ACCEPT_ALL_TARGETS = [
    (1292, 600), (1319, 286), (1292, 595), (1165, 641), (1135, 650), (1150, 650)
]

def execute_accept_all():
    print(f"[{time.strftime('%H:%M:%S')}] Executing Accept All...")
    try:
        fire_omni_f8()
        orig_pos = win32api.GetCursorPos()
        for tx, ty in ACCEPT_ALL_TARGETS:
            win32api.SetCursorPos((tx, ty))
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            time.sleep(0.01)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            time.sleep(0.01)
        win32api.SetCursorPos(orig_pos)
    except Exception as e:
        print(f"Error in execution: {e}")

if __name__ == "__main__":
    print(f"[{time.strftime('%H:%M:%S')}] PHOENIX SNIPER STARTING...")
    while True:
        try:
            with open(HB_FILE, "w") as f:
                f.write(str(time.time()))
            print(f"[{time.strftime('%H:%M:%S')}] Heartbeat updated: {HB_FILE}")
        except Exception as e:
            print(f"Heartbeat write error: {e}")

        execute_accept_all()
        time.sleep(30.0)
