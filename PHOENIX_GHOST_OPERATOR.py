# -*- coding: utf-8 -*-
import ctypes
import time
import os
import win32api
import win32con

# PHOENIX GHOST OPERATOR v1.1 [受容接続・離席偽装]
# 師匠の命：マウスの微細な信号を送り、PCが動いているとOSに誤認識させる。
# ただし、PCを重くしないよう、更新リズムを調整。

PROTOCOL_DIR = r"P:/"
HEARTBEAT_FILE = r"P:\PHOENIX_HEARTBEATS\hb_Receptor.txt"
TRIGGER_FILE = r"P:\PHOENIX_GHOST_TRIGGER.txt"

if __name__ == "__main__":
    try: ctypes.windll.kernel32.SetConsoleTitleW("PHOENIX_GHOST_OPERATOR")
    except: pass
    
    print("--- PHOENIX 受容接続：点火 ---")
    while True:
        try:
            # 「白紙」トリガーがあれば擬似操作
            if os.path.exists(TRIGGER_FILE):
                win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 0, 0, 0, 0)
            
            # 師匠の命：心臓（Heartbeat）を刻む
            with open(HEARTBEAT_FILE, "w") as f:
                f.write(str(time.time()))
        except: pass
        time.sleep(60) # 1分おきの深い呼吸
