import time
import datetime
import win32api
import win32con

def terminal_pure_f8_loop():
    """
    ターミナル上で「F8を押しました」と5秒ごとに表示しつつ、
    実際に win32api でF8を送信する。
    """
    VK_F8 = 0x77
    
    print("=========================================")
    print(" 【5秒ごとのF8ターミナル出力プログラム】")
    print("  ターミナルをアクティブにした状態で開始します。")
    print("=========================================\n")
    
    count = 1
    while True:
        # F8の押下と解放
        win32api.keybd_event(VK_F8, 0, 0, 0)
        time.sleep(0.05)
        win32api.keybd_event(VK_F8, 0, win32con.KEYEVENTF_KEYUP, 0)
        
        # 画面に確実に出力
        print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] F8を押しました。 (回数: {count})")
        
        count += 1
        time.sleep(5)

if __name__ == "__main__":
    terminal_pure_f8_loop()
