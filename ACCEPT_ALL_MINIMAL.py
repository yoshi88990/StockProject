import ctypes
import time
import win32api
import win32con
import sys
import os
import win32gui

# --- PHOENIX SNIPER: OM-STRIKE [SACRED CHRONO DNA] Ver 36.1 ---
# 師匠の命：STOP_PHOENIX 信号を尊重し、最小化中は絶対に動かない。
STOP_SIGNAL = r"P:\STOP_PHOENIX"

class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]

def get_idle_time():
    lii = LASTINPUTINFO()
    lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
    ctypes.windll.user32.GetLastInputInfo(ctypes.pointer(lii))
    return (ctypes.windll.kernel32.GetTickCount() - lii.dwTime) / 1000.0

def log_vision(msg):
    try:
        with open(r"P:\sniper_vision.txt", "a", encoding="utf-8") as f:
            f.write(f"{time.strftime('%H:%M:%S')} - {msg}\n")
    except: pass

def is_user_operating(orig_pos):
    """
    【絶対軽量化・フリーズ防止版】
    重いハードウェアポーリング(GetAsyncKeyState)を完全廃止し、
    OS全体の最終入力時間(GetLastInputInfo)と現在カーソルのみで瞬時に判定。
    """
    curr_pos = win32api.GetCursorPos()
    # マウスが1pxでも動いていたら操作中とみなす
    if abs(curr_pos[0] - orig_pos[0]) > 1 or abs(curr_pos[1] - orig_pos[1]) > 1:
        return True
    
    # OS全体のキー/マウス操作アイドル時間が0.5秒未満なら「操作中」とみなす
    if get_idle_time() < 0.5:
        return True
        
    return False

def strike_ritual(tx, ty, label, use_f8=True):
    try:
        orig_pos = win32api.GetCursorPos()
        # 【超・謙虚】射撃前の「ご操作」を0.5秒間厳格に監視
        if is_user_operating(orig_pos):
            log_vision(f"ABORT[{label}]: 師匠のご操作を検知。腕を引きます。")
            return

        win32api.SetCursorPos((tx, ty))
        time.sleep(0.01)

        # 【超・謙虚：キーボード干渉の完全排除】
        # 以前はここで Alt+Enter や F8 を送信していましたが、
        # これが「文字が打てなくなる（キーボードショートカット暴発）」の
        # 真の原因だったため、物理キー偽装を完全に削除しました。


        # 3. 師匠の二連射
        time.sleep(0.01)
        for _ in range(2):
            ctypes.windll.user32.mouse_event(0x0002, 0, 0, 0, 0)
            time.sleep(0.01)
            ctypes.windll.user32.mouse_event(0x0004, 0, 0, 0, 0)
            time.sleep(0.01)
            
        win32api.SetCursorPos(orig_pos)
        log_vision(f"HIT[{label}]: ({tx},{ty})")
    except Exception as e:
        log_vision(f"ERROR: {e}")

def execute_mechanical_static_snipe():
    if get_idle_time() < 5.0: return 

    current_time = time.time()
    global last_static_time
    if 'last_static_time' not in globals(): last_static_time = 0

    # ② 固定座標 (1分おき) - これが真の「機械打ち(固定)」の姿
    if current_time - last_static_time >= 60.0:
        for tx, ty in [(1319, 286), (1292, 595), (1165, 641), (1135, 650), (1150, 650), (1167, 636)]:
            strike_ritual(tx, ty, "②_FIXED")
        last_static_time = current_time

def find_antigravity_window():
    hl = []
    win32gui.EnumWindows(lambda h, e: hl.append(h) if "Antigravity" in win32gui.GetWindowText(h) else None, None)
    return hl[0] if hl else None

if __name__ == "__main__":
    try: ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x00000020)
    except: pass
    
    ag_hwnd = None
    esc_press_start = 0
    
    while True:
        try:
            with open(r"P:\PHOENIX_HEARTBEATS\hb_Mechanical.txt", "w") as f: f.write(str(time.time()))
            
            if ag_hwnd is None or not win32gui.IsWindow(ag_hwnd): ag_hwnd = find_antigravity_window()
            
            fg_hwnd = win32gui.GetForegroundWindow()
            is_min = win32gui.IsIconic(ag_hwnd) if ag_hwnd else True
            is_ag_fg = (fg_hwnd == ag_hwnd)
            
            # 【絶対律】最小化中、あるいは停止信号がある間は「腕」をピクリとも動かさない
            if not is_min and not os.path.exists(STOP_SIGNAL):
                execute_mechanical_static_snipe()
                
            if win32api.GetAsyncKeyState(0x1B) & 0x8000:
                if esc_press_start == 0: esc_press_start = time.time()
                if time.time() - esc_press_start >= 1.0: sys.exit(0)
            else: esc_press_start = 0
                
        except Exception: ag_hwnd = None
        time.sleep(0.1)
