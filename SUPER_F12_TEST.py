import win32api
import win32con
import time
import sys

# 標準出力を設定
sys.stdout.reconfigure(encoding='utf-8')

def super_f12_press():
    """ 
    最も標準的かつ強力な Virtual Key (VK) 方式で F12 を叩く。
    多くのホットキーソフトはこの方式を監視している。
    """
    VK_F12 = 0x7B
    
    # Press
    win32api.keybd_event(VK_F12, 0, 0, 0)
    time.sleep(0.05)
    # Release
    win32api.keybd_event(VK_F12, 0, win32con.KEYEVENTF_KEYUP, 0)
    print("F12 (VK) Shot!")

if __name__ == "__main__":
    print("!!! 究極打鍵テスト：F12 を 5回連射します !!!")
    for i in range(5):
        super_f12_press()
        time.sleep(0.5)
