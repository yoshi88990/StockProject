import win32gui
import win32con
import win32api

def ghost_click_window(window_title, x, y):
    """
    対象ウィンドウに物理マウスを動かさず直接クリックシグナルを送り込む
    """
    # ウィンドウのハンドル（識別ID）を裏側から取得
    hwnd = win32gui.FindWindow(None, window_title)
    
    if hwnd:
        # LParamは X座標とY座標をビット演算で1つの値に結合したもの
        lparam = (y << 16) | x
        
        # PostMessageにより、バックグラウンドのまま左クリックダウン＆アップ信号を送信
        win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lparam)
        win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0, lparam)
        print(f"Ghost operation successful on `{window_title}` at ({x}, {y}).")
        return True
    else:
        print(f"Target window '{window_title}' invisible to ghost protocol.")
        return False

if __name__ == "__main__":
    print("【GHOST_PROTOCOL】モジュール初期化完了。")
    print("使用法: ghost_click_window('ウィンドウ名', x座標, y座標)")
