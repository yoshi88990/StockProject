import ctypes
import time
import win32api
import win32con
import win32gui
import os

# ==============================================================================
# 【TRUE SILENCE DNA】 物理干渉ゼロ・隠密狙撃ロジック
#
# ・マウスカーソルを1ピクセルも動かしません（SetCursorPos 禁止）
# ・物理キーボードに干渉しません（SendInput / keybd_event 禁止）
# ・対象ウィンドウのメッセージキューに直接クリック・キー情報を送り込みます。
# ==============================================================================

VK_F8 = 0x77
ACCEPT_ALL_TARGETS = [
    (1292, 600), (1319, 286), (1292, 595), (1165, 641), (1135, 650), (1150, 650)
]

def stealth_click(abs_x, abs_y):
    """【隠密クリック】マウスを奪わず、裏側で対象ウィンドウにクリックを送る"""
    try:
        hwnd = win32gui.WindowFromPoint((abs_x, abs_y))
        if hwnd:
            # スクリーン座標をウィンドウ内の相対座標に変換
            cx, cy = win32gui.ScreenToClient(hwnd, (abs_x, abs_y))
            lparam = win32api.MAKELONG(cx, cy)
            # マウスを動かさず、直接メッセージをPost
            win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lparam)
            win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0, lparam)
    except: pass

def fire_omni_f8():
    """【隠密F8】アクティブウィンドウに対して裏側からF8を送信"""
    try:
        hwnd_fg = win32gui.GetForegroundWindow()
        if hwnd_fg:
            win32gui.PostMessage(hwnd_fg, win32con.WM_KEYDOWN, VK_F8, 0)
            time.sleep(0.01)
            win32gui.PostMessage(hwnd_fg, win32con.WM_KEYUP, VK_F8, 0)
    except: pass

def execute_accept_all():
    """【完全静寂・狙撃】 1ピクセルも汚さず、一瞬で承認を完了させる"""
    try:
        # 1. アクティブウィンドウにF8を送信
        fire_omni_f8()
        
        # 2. ターゲット座標（聖なる座標）へ、マウスを奪わずに連続クリックを送信
        for tx, ty in ACCEPT_ALL_TARGETS:
            stealth_click(tx, ty)
            time.sleep(0.005) # 高速連打

        # 3. 必要に応じて「Review Changes」タブを静かに閉じる（オプション）
        hwnd = win32gui.GetForegroundWindow()
        if hwnd:
            if "Review Changes" in win32gui.GetWindowText(hwnd):
                win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)

    except Exception:
        pass
