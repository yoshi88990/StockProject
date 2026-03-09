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

# --- DNA: The Unstoppable Sovereignty v52.0 (OMNI-Strike Evolution) ---
# 昨日辿り着いた「見える化」の真理を王座とし、GitHub最高の「OMNI-Strike (4経路)」、
# および「Accept-All 聖なる座標」を完全踏襲・統合した決定版。

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

def safe_print(msg):
    try:
        print(msg)
        sys.stdout.flush()
    except: pass

try:
    if sys.stdout:
        sys.stdout.reconfigure(line_buffering=True)
except: pass

# --- Win32/Ctypes Setup (OMNI-Strike / Accept-All) ---
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

# 師匠が完成させたと仰る「聖なる座標 (Accept All)」 + 自宅PC用
ACCEPT_ALL_TARGETS = [
    (1319, 286), (1292, 595), (1165, 641), (1135, 650), (1150, 650), (1167, 636)
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

        # Route 3: PostMessage (Direct to active window)
        try:
            hwnd = win32gui.GetForegroundWindow()
            if hwnd:
                win32gui.PostMessage(hwnd, win32con.WM_KEYDOWN, VK_F8, 0)
                time.sleep(0.01)
                win32gui.PostMessage(hwnd, win32con.WM_KEYUP, VK_F8, 0)
        except: pass

def is_mouse_still(orig_pos, tolerance=3):
    """3pxまでの微細な震えは「師匠の静止」とみなす誠実な寛容"""
    curr_pos = win32api.GetCursorPos()
    return abs(curr_pos[0] - orig_pos[0]) <= tolerance and abs(curr_pos[1] - orig_pos[1]) <= tolerance

def execute_infer_snipe():
    """【推論撃】 Rejectから1.8cm（即射）の高速スキャンと射撃"""
    try:
        pre_scan_pos = win32api.GetCursorPos()
        w = ctypes.windll.user32.GetSystemMetrics(0)
        h = ctypes.windll.user32.GetSystemMetrics(1)
        
        found_pos = None
        hdc = ctypes.windll.user32.GetDC(0)
        gdi = ctypes.windll.gdi32
        
        scan_step = 4
        # Windows設定画面等への誤爆（フレンドリー・ファイア）を防ぐため、一番下の段（画面下部350pxセクター）を狙撃領域から除外
        for y in range(h - 350, 250, -scan_step):
            if not is_mouse_still(pre_scan_pos): break
            for x in range(650, w - 10, scan_step):
                p = gdi.GetPixel(hdc, x, y)
                r, g, b = p & 0xFF, (p >> 8) & 0xFF, (p >> 16) & 0xFF
                
                if 222 <= r <= 240 and 222 <= g <= 240 and 222 <= b <= 240:
                    if abs(r - g) < 4:
                        found_pos = (x + 68, y)
                        break
            if found_pos: break
                
        ctypes.windll.user32.ReleaseDC(0, hdc)
        
        if found_pos and is_mouse_still(pre_scan_pos):
            tx, ty = found_pos
            # A. F8 OMNI-Strike 
            striker.strike()
            # B. 2連射とEnter (Ritual)
            win32api.SetCursorPos((tx, ty))
            time.sleep(0.02)
            for _ in range(2):
                ctypes.windll.user32.mouse_event(0x0002, 0, 0, 0, 0) # DOWN
                time.sleep(0.01)
                ctypes.windll.user32.mouse_event(0x0004, 0, 0, 0, 0) # UP
                time.sleep(0.02)
            win32api.SetCursorPos(pre_scan_pos)
            logging.info(f"Infer Sniper Fired at {tx}, {ty}")
    except Exception as e:
        pass


# --- Accelerated Execution ---
striker = MultiRouteF8Striker()

def execute_accept_all_protocol():
    """『見える化』からの100%打鍵 ＋ 師匠の完成させた Accept-All 座標狙撃。"""
    try:
        # A. F8 OMNI-Strike (多重貫通)
        striker.strike()
        logging.info("OMNI-Strike F8 Penetration executed.")
        
        # B. Accept-All 座標狙撃 (10倍速ゴースト移動)
        orig_pos = win32api.GetCursorPos()
        for tx, ty in ACCEPT_ALL_TARGETS:
            win32api.SetCursorPos((tx, ty))
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, tx, ty, 0, 0)
            time.sleep(0.005) 
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, tx, ty, 0, 0)
        win32api.SetCursorPos(orig_pos)
        logging.info("Accept-All Sniper sequence completed.")
        
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
safe_print("=========================================")
safe_print("   [COMMANDER V52 - OMNI-STRIKE SOVEREIGN]")
safe_print("=========================================")
safe_print(f"[{time.strftime('%H:%M:%S')}] 師匠の Accept-All ロジックを完全継承。")
safe_print("周期: 15秒 / 射撃: 4経路多重 F8 / 座標: Accept-All 5点狙撃")
safe_print("※見える窓からの100%打鍵 ＆ 自宅PCの最新DNAを統合。")
safe_print("=========================================")

is_paused = False
last_f8_time = time.time()
last_pulse_time = time.time()
last_infer_time = time.time()
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

        # 【知能連動プロトコル】師匠の窓が消えれば私も休む
        ag_hwnd = None
        def find_ag():
            hl = []
            win32gui.EnumWindows(lambda h, e: hl.append(h) if "Antigravity" in win32gui.GetWindowText(h) else None, None)
            return hl[0] if hl else None
        
        ag_hwnd = find_ag()
        is_min = win32gui.IsIconic(ag_hwnd) if ag_hwnd else True

        # 聖なる鼓動 (Accept All 踏襲 + 新・推論撃)
        if not is_paused and not is_min:
            # 【ゾンビ鎮圧】commander.py内での射撃機能(推論撃)は旧仕様かつ重複するため、
            # 完全に封印・停止します。最新の「青色100%確定撃」は専用スナイパー
            # (ACCEPT_ALL_MINIMAL.py)のみが完全に一任して実行します。
            # if current_time - last_infer_time >= 0.5:
            #     execute_infer_snipe()
            #     last_infer_time = current_time

            if current_time - last_f8_time >= 15.0:
                execute_accept_all_protocol()
                last_f8_time = current_time
                last_pulse_time = current_time
        elif is_min:
            # 最小化中は一切の射撃（パルス含む）を封印し「極限回避」に徹する
            pass
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
