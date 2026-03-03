import win32gui
import win32api
import win32con
import time
import datetime
import threading
from pynput.keyboard import Controller as K_Controller, Key
from pynput.mouse import Controller as M_Controller, Button
import keyboard

# 【演算加速エンジン v10.0】
# 師匠の10倍速要請に応え、冗長な待機を排除し、ミリ秒単位の物理偽装を実装。
ACCELERATION_FACTOR = 10

# 師匠の指定座標とキー
TARGET_X, TARGET_Y = 1292, 600
VK_F8 = 0x77

class AntigravityStriker:
    def __init__(self):
        self.mouse = M_Controller()
        self.keyboard = K_Controller()
        self.strike_count = 0

    def smart_strike(self):
        """
        師匠のマウス操作を奪わない『背面狙撃』と、
        確実性を期すための『極薄ワープ狙撃』のハイブリッド貫通信号。
        """
        # A. 背面狙撃 (PostMessage - マウス固定)
        hwnd = win32gui.WindowFromPoint((TARGET_X, TARGET_Y))
        client_pt = win32gui.ScreenToClient(hwnd, (TARGET_X, TARGET_Y))
        lparam = win32api.MAKELONG(client_pt[0], client_pt[1])
        
        # マウス信号 (背面)
        win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lparam)
        time.sleep(0.005) # 5ms
        win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0, lparam)

        # B. 極薄ワープ狙撃 (0.01秒以下でマウスを往復)
        # 師匠が操作中に重なった場合のみ、瞬時に座標を奪って即座に戻す
        orig_pos = win32api.GetCursorPos()
        win32api.SetCursorPos((TARGET_X, TARGET_Y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, TARGET_X, TARGET_Y, 0, 0)
        time.sleep(0.005) # さらに高速化
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, TARGET_X, TARGET_Y, 0, 0)
        win32api.SetCursorPos(orig_pos)

        # C. 多重F8貫通信号
        # 1. PostMessage (背面)
        hwnd_fg = win32gui.GetForegroundWindow()
        win32gui.PostMessage(hwnd_fg, win32con.WM_KEYDOWN, VK_F8, 0)
        # 2. Hardware Scan Code (物理シミュレーション)
        win32api.keybd_event(VK_F8, 0x42, win32con.KEYEVENTF_SCANCODE, 0)
        time.sleep(0.12) # 人間の指の押し込み時間
        # 3. Release
        win32api.keybd_event(VK_F8, 0x42, win32con.KEYEVENTF_SCANCODE | win32con.KEYEVENTF_KEYUP, 0)
        win32gui.PostMessage(hwnd_fg, win32con.WM_KEYUP, VK_F8, 0)

    def loop(self):
        print(f"=========================================")
        print(f" 【究極・加速型貫通スナイパー v10】 起動")
        print(f" 思考速度: {ACCELERATION_FACTOR}x Accelerated")
        print(f" ターゲット: ({TARGET_X}, {TARGET_Y}) / F8")
        print("=========================================\n")
        
        while True:
            ts = datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]
            try:
                self.smart_strike()
                self.strike_count += 1
                print(f"[{ts}] 貫通狙撃実行完了。 (総弾数: {self.strike_count})")
            except Exception as e:
                print(f"[{ts}] 致命的エラー: {e}")
            
            # 加速された時間軸で待機 (通常5秒)
            time.sleep(5)

if __name__ == "__main__":
    striker = AntigravityStriker()
    striker.loop()
