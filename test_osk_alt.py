import ctypes
import time
import win32api
import win32con

OSK_LEFT_COORD = (1265, 322) # 新しい左Altキーの座標
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004

print("【テスト開始】スクリーンキーボードの左Alt（1265, 322）を1回だけクリックします...")
orig_mouse = win32api.GetCursorPos()

# 1. マウスを移動し、微小待機（UIに「ホバーした」と認識させる）
win32api.SetCursorPos(OSK_LEFT_COORD)
time.sleep(0.05)

# 2. 押し込んで、クリック状態を確実にするため少し長めに待つ
ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
time.sleep(0.05) 

# 3. 離して、離したことが伝わるまで待つ
ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
time.sleep(0.05)

# 4. 元の位置へ復帰
win32api.SetCursorPos(orig_mouse)

print("【テスト完了】1発のみの狙撃が終わりました。")
