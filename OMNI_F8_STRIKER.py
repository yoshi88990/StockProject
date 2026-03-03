import ctypes
import time
import win32api
import win32con
import win32gui

# F8キー定義
SCAN_F8 = 0x42
VK_F8 = 0x77
KEYEVENTF_SCANCODE = 0x0008
KEYEVENTF_KEYUP = 0x0002

# win32 構造体定義 (SCAN用)
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

class MultiRouteF8Striker:
    """
    あらゆる防壁を想定し、4つの異なる経路から「F8打鍵」を流し込む。
    一つのルートがブロックされても、別のルートが成功すれば目的を完遂できる。
    """

    def route_1_hardware_scan(self):
        """【ルート1】ctypes物理スキャンコード (最深部)"""
        try:
            extra = ctypes.c_ulong(0)
            ii_ = Input_I()
            # Press
            ii_.ki = KeyBdInput(0, SCAN_F8, KEYEVENTF_SCANCODE, 0, ctypes.pointer(extra))
            x = Input(ctypes.c_ulong(1), ii_)
            ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
            time.sleep(0.05)
            # Release
            ii_.ki = KeyBdInput(0, SCAN_F8, KEYEVENTF_SCANCODE | KEYEVENTF_KEYUP, 0, ctypes.pointer(extra))
            x = Input(ctypes.c_ulong(1), ii_)
            ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
            return True
        except Exception:
            return False

    def route_2_virtual_key(self):
        """【ルート2】win32api仮想キー (OS標準)"""
        try:
            win32api.keybd_event(VK_F8, 0, 0, 0)
            time.sleep(0.05)
            win32api.keybd_event(VK_F8, 0, win32con.KEYEVENTF_KEYUP, 0)
            return True
        except Exception:
            return False

    def route_3_direct_message(self, target_hwnd=None):
        """【ルート3】SendMessage (ゴースト・API直叩き)"""
        try:
            # hwndが指定されていなければ、アクティブウィンドウをターゲットにする
            hwnd = target_hwnd if target_hwnd else win32gui.GetForegroundWindow()
            if hwnd:
                win32gui.PostMessage(hwnd, win32con.WM_KEYDOWN, VK_F8, 0)
                time.sleep(0.05)
                win32gui.PostMessage(hwnd, win32con.WM_KEYUP, VK_F8, 0)
                return True
            return False
        except Exception:
            return False

    def route_4_pydirectinput(self):
        """【ルート4】DirectX対応高レイヤー入力"""
        try:
            import pydirectinput
            pydirectinput.press('f8')
            return True
        except ImportError:
            # ライブラリが無い場合はスキップ（これ自体がフェールセーフ）
            return False
        except Exception:
            return False

    def unyielding_strike(self):
        """全ルート同時発射による絶対完遂"""
        print("【OMNI_F8_STRIKE】 多重経路でのF8送出を開始します。")
        success_count = 0
        
        if self.route_1_hardware_scan(): success_count += 1
        if self.route_2_virtual_key(): success_count += 1
        if self.route_3_direct_message(): success_count += 1
        if self.route_4_pydirectinput(): success_count += 1
        
        print(f"【STRIKE_REPORT】 送信完了。{success_count}/4 のルートが正常に稼働しました。")
        return success_count > 0

if __name__ == "__main__":
    striker = MultiRouteF8Striker()
    striker.unyielding_strike()
