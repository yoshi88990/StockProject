import win32api
import win32con
import time
import datetime

def unstoppable_f8_loop():
    """
    【絶対F8ループ】
    5秒に1回、確実にF8を打ち込み続ける。
    ターミナル上で動かすことで、Windowsの防壁を突破してソフトへとF8を届かせる。
    """
    VK_F8 = 0x77
    
    print("==================================================")
    print(" 【絶対F8ループ】起動完了")
    print(" 5秒間隔でF8の打鍵を開始します...")
    print(" 停止するにはこのウィンドウを選択し、Ctrl+Cを押してください。")
    print("==================================================")
    
    try:
        count = 1
        while True:
            # F8を押す
            win32api.keybd_event(VK_F8, 0, 0, 0)
            time.sleep(0.05)
            # F8を離す
            win32api.keybd_event(VK_F8, 0, win32con.KEYEVENTF_KEYUP, 0)
            
            timestamp = datetime.datetime.now().strftime('%H:%M:%S')
            print(f"[{timestamp}] {count}回目のF8を送信しました。")
            
            count += 1
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\n絶対F8ループを停止しました。")

if __name__ == "__main__":
    unstoppable_f8_loop()
