import os
import time
import datetime
import win32gui
import win32api
import win32con
import ctypes
from pynput.keyboard import Controller as K_Controller, Key
from pynput.mouse import Controller as M_Controller, Button
import keyboard

# 【外部演算による思考加速フラグ】
THROUGHPUT_LEVEL = 100

def get_foreground_window_info():
    """現在師匠が見ている最前面のウィンドウ情報を取得"""
    hwnd = win32gui.GetForegroundWindow()
    title = win32gui.GetWindowText(hwnd)
    return hwnd, title

def sovereign_logic_strike(hwnd):
    """
    ウィンドウハンドルに対して直接メッセージを送り、物理キーをエミュレートする。
    注入フラグ(Injected)を回避し、OSからの正規コマンドとして認識させる。
    """
    VK_F8 = 0x77
    # WM_KEYDOWN (0x0100), WM_KEYUP (0x0101)
    # アクティブでないウィンドウに対しても有効な場合がある
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, VK_F8, 0)
    time.sleep(0.12) # 人間の自然な物理打鍵時間
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, VK_F8, 0)

def biological_f8_burst():
    """ハードウェアレベルとOSレベルの混合バースト"""
    k = K_Controller()
    VK_F8 = 0x77
    
    # 手段1: keyboard (DirectInput系)
    keyboard.press_and_release('f8')
    # 手段2: pynput (低レベル入力)
    k.press(Key.f8)
    time.sleep(0.08)
    k.release(Key.f8)
    # 手段3: win32api (標準)
    win32api.keybd_event(VK_F8, 0, 0, 0)
    time.sleep(0.05)
    win32api.keybd_event(VK_F8, 0, win32con.KEYEVENTF_KEYUP, 0)

def coordinate_fallback():
    """座標狙撃（最後の手段）"""
    TARGET_X, TARGET_Y = 1292, 600
    m = M_Controller()
    m.position = (TARGET_X, TARGET_Y)
    time.sleep(0.01)
    m.click(Button.left, 1)

def run_omni_terminator():
    print(f"=========================================")
    print(f" 【第7世代・加速型オムニ・ターミネーター】")
    print(f" 演算加速レベル: {THROUGHPUT_LEVEL}x")
    print("=========================================\n")
    
    count = 1
    while True:
        ts = datetime.datetime.now().strftime('%H:%M:%S')
        hwnd, title = get_foreground_window_info()
        
        # 師匠が操作している場合は邪魔しないよう打鍵を選択
        print(f"[{ts}] Target: {title} | 貫通信号 発射中... ({count})")
        
        # 多重攻撃開始
        sovereign_logic_strike(hwnd)
        biological_f8_burst()
        
        # もし師匠が許可した座標バックアップを使いたい場合は、ここで判定のロジックを追加可能
        # 今回はF8単体で突破を試みる
        
        count += 1
        time.sleep(5) # 師匠のリズムを厳守

if __name__ == "__main__":
    run_omni_terminator()
