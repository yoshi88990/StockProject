import mss
import numpy as np
import win32api
import win32con
import time

def lightweight_pixel_snipe(target_bgr, region=None):
    """
    指定領域内の特定ピクセルカラー（BGR）を最軽量で探し出し、撃ち抜く
    target_bgr: (Blue, Green, Red)の値
    region: {'top': 0, 'left': 0, 'width': 1920, 'height': 1080} のような辞書
    """
    with mss.mss() as sct:
        monitor = region if region else sct.monitors[1] # メインモニター全体か指定領域
        # 超高速でキャプチャしNumPy配列化 (BGRA形式)
        img = np.array(sct.grab(monitor))
        
        # ターゲットのBGRと完全一致する座標を抽出
        matches = np.where((img[:, :, 0] == target_bgr[0]) & 
                           (img[:, :, 1] == target_bgr[1]) & 
                           (img[:, :, 2] == target_bgr[2]))
        
        if len(matches[0]) > 0:
            # 最初の発見座標
            y, x = matches[0][0], matches[1][0]
            screen_x = x + monitor['left']
            screen_y = y + monitor['top']
            
            # 物理クリック発動
            win32api.SetCursorPos((screen_x, screen_y))
            time.sleep(0.01)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, screen_x, screen_y, 0, 0)
            time.sleep(0.01)
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, screen_x, screen_y, 0, 0)
            print(f"Target Acquired and Sniped at: ({screen_x}, {screen_y})")
            return True
            
    return False

if __name__ == "__main__":
    print("【LIGHTWEIGHT_SNIPER】モジュール初期化完了。")
    print("テスト用のダミー実行待機...")
    # example: lightweight_pixel_snipe([0, 0, 255]) # 赤色を探す
