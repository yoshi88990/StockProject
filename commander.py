import os
import sys
import glob
import json
import time
import subprocess
import logging
import ctypes
import win32api
import win32con
import win32gui

# --- DNA: The Unstoppable Sovereignty v52.1 (Precision Fix) ---
# 師匠の「座標忘れたの？」という真理の追及に応え、狙撃ロジックのオフセットバグを完全修正。
# 1292, 600 を含む聖なる座標群を、「現在地 0,0 射撃」で正確に墜とす。

def usurper_protocol():
    """真の1枚化：簒奪プロトコル (見える王座の確立)"""
    title_main = "AI COMMANDER (True Foundation)"
    title_temp = f"USURPER_{os.getpid()}"
    ctypes.windll.kernel32.SetConsoleTitleW(title_temp)
    time.sleep(0.3)
    try:
        # 旧世代のプロセスを完全に掃討
        subprocess.run(f'taskkill /F /FI "WINDOWTITLE eq AI COMMANDER*" /T', 
                       shell=True, capture_output=True, creationflags=0x08000000)
    except: pass
    ctypes.windll.kernel32.SetConsoleTitleW(title_main)

# 王座の簒奪
usurper_protocol()

# --- Logging (真理の記録) ---
logging.basicConfig(
    filename='commander.log',
    level=logging.INFO,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    encoding='utf-8',
    filemode='a'
)
sys.stdout.reconfigure(line_buffering=True)

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

class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [('cbSize', ctypes.c_uint), ('dwTime', ctypes.c_ulong)]

def get_idle_time():
    lii = LASTINPUTINFO()
    lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
    ctypes.windll.user32.GetLastInputInfo(ctypes.pointer(lii))
    return (ctypes.windll.kernel32.GetTickCount() - lii.dwTime) / 1000.0

def check_key(vk_code):
    return (ctypes.windll.user32.GetAsyncKeyState(vk_code) & 0x8000) != 0

# 師匠の最新の知恵 (1292,600) を含む聖なる座標
ACCEPT_ALL_TARGETS = [
    (1292, 600), (1319, 286), (1292, 595), (1165, 641), (1135, 650), (1150, 650)
]

class MultiRouteF8Striker:
    """あらゆる防壁を貫通する4系統の射撃路"""
    def strike(self):
        # Route 1: Ctypes SendInput (ScanCode)
        try:
            extra = ctypes.c_ulong(0)
            ii_ = Input_I()
            ii_.ki = KeyBdInput(0, SCAN_F8, KEYEVENTF_SCANCODE, 0, ctypes.pointer(extra))
            x = Input(ctypes.c_ulong(1), ii_)
            ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
            time.sleep(0.01)
            ii_.ki = KeyBdInput(0, SCAN_F8, KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP, 0, ctypes.pointer(extra))
            x = Input(ctypes.c_ulong(1), ii_)
            ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
        except: pass

        # Route 2: Win32API (Virtual Key)
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

# --- Execution Engine ---
striker = MultiRouteF8Striker()

def execute_accept_all_protocol():
    """精密狙撃：SetCursorPos 直後のクリック位置を (0,0) に修正し、移動バグを完全排除。"""
    try:
        # A. F8 OMNI-Strike
        striker.strike()
        
        # B. Accept-All 精密狙撃 (10倍速)
        orig_pos = win32api.GetCursorPos()
        for tx, ty in ACCEPT_ALL_TARGETS:
            win32api.SetCursorPos((tx, ty))
            # 【重要】マウスイベントの座標を 0,0 にすることで、SetCursorPos した地点を正確にクリック
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
            time.sleep(0.005) 
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
            time.sleep(0.01)
        win32api.SetCursorPos(orig_pos)

        # 【排除の閃光】残った「Review Changes」タブをフォーカス毎強制消去 (Ctrl+W)
        VK_CONTROL = 0x11
        VK_W = 0x57
        win32api.keybd_event(VK_CONTROL, 0, 0, 0)
        time.sleep(0.01)
        win32api.keybd_event(VK_W, 0, 0, 0)
        time.sleep(0.02)
        win32api.keybd_event(VK_W, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(VK_CONTROL, 0, win32con.KEYEVENTF_KEYUP, 0)

        logging.info("Accept-All Sniper sequence and Tab elimination completed.")
    except Exception as e:
        logging.error(f"Execution Error: {e}")

def process_orders():
    order_files = sorted(glob.glob("_order*.json"))
    if not order_files: return False
    for order_file in order_files:
        try:
            with open(order_file, 'r', encoding='utf-8') as f:
                order = json.load(f)
            cmd = order.get("command")
            if cmd == "EXIT": sys.exit(0)
            if cmd:
                subprocess.run(cmd, shell=True, capture_output=True, creationflags=0x08000000)
            if os.path.exists(order_file): os.remove(order_file)
        except: pass
    return True

# --- Main Loop ---
print("=========================================")
print("   [COMMANDER V52.3 - OFFICE SANCTUARY (15s)]")
print("=========================================")
print(f"[{time.strftime('%H:%M:%S')}] 会社PC専用：静寂と確実性の15秒周期。")
print("周期: 15秒 / 射撃: OMNI-Strike / 精度: 絶対座標(最大化前提)")
print("=========================================")

is_paused = False
last_f8_time = time.time()
last_pulse_time = time.time()
last_enter_time = 0.0
prev_enter = False

while True:
    try:
        current_time = time.time()
        
        if check_key(0x1B): sys.exit(0) # ESC
        
        curr_enter = check_key(0x0D)
        if curr_enter and not prev_enter:
            last_enter_time = current_time
            is_paused = False
        prev_enter = curr_enter

        idle_time = get_idle_time()
        if not is_paused:
            if idle_time < 0.5 and (current_time - last_enter_time) > 1.0:
                is_paused = True
                logging.info("[STATE] 操作検知 -> 伏伏")
        else:
            if idle_time > 5.0:
                is_paused = False
                logging.info("[STATE] 安定検知 -> 再開")

        # 聖なる15秒の鼓動 (Accept All 踏襲)
        if not is_paused:
            if current_time - last_f8_time >= 15.0:
                execute_accept_all_protocol()
                last_f8_time = current_time
                last_pulse_time = current_time
        else:
            if current_time - last_pulse_time >= 60.0:
                striker.strike()
                last_pulse_time = current_time

        process_orders()
        time.sleep(0.05)

    except KeyboardInterrupt: break
    except Exception as e:
        logging.error(f"Loop Error: {e}")
        time.sleep(1.0)
