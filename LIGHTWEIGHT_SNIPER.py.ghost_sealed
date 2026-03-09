import mss
import numpy as np
import win32api
import win32con
import time

def lightweight_pixel_snipe(target_bgr, region=None, dry_run=False):
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
            if not dry_run:
                time.sleep(0.01)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, screen_x, screen_y, 0, 0)
                time.sleep(0.01)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, screen_x, screen_y, 0, 0)
                print(f"Target Acquired and Sniped (CLICKED) at: ({screen_x}, {screen_y})")
            else:
                print(f"Target Acquired (DRY RUN - Moved Mouse Only) at: ({screen_x}, {screen_y})")
            return True
            
    return False

if __name__ == "__main__":
    print("=== 【LIGHTWEIGHT_SNIPER】 照準テスト開始 ===")
    print("現在画面上にある「完全な白色 [255, 255, 255]」のピクセルを弾き出し、マウスを移動させます。")
    print("安全のためクリックは行わず、マウスカーソルの移動（照準合わせ）のみ実行します...")
    
    # テスト開始まで3秒待機（ユーザーが画面の準備をするため）
    for i in range(3, 0, -1):
        print(f"スキャン開始まで {i} 秒...")
        time.sleep(1)
        
    start_time = time.time()
    # テストとして白色(BGR: 255, 255, 255)を探す
    found = lightweight_pixel_snipe([255, 255, 255], dry_run=True)
    end_time = time.time()
    
    if found:
        print(f"【成功】標的の捕捉に成功しました！ 索敵時間: {end_time - start_time:.4f} 秒")
    else:
        print("【失敗】指定された色の標的が画面内に見つかりませんでした。")
