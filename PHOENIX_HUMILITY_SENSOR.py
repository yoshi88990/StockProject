# -*- coding: utf-8 -*-
import os
import time
import ctypes
import re

# PHOENIX HUMILITY SENSOR v1.1 [誠実さの監視・傲慢度監査]
# 師匠の命：AIが勝手に「重い」挙動をしたり、ルールを書き換えたりしないか監視。
# PCを重くしないよう、60秒に1回、静かに目を光らせる。

PROTOCOL_DIR = r"P:/"
SNIPER_PATH = os.path.join(PROTOCOL_DIR, "ACCEPT_ALL_MINIMAL.py")
VAULT_DIR = os.path.join(PROTOCOL_DIR, "DNA_VAULT")
SCORE_FILE = os.path.join(VAULT_DIR, "current_arrogance.txt")
HEARTBEAT_FILE = r"P:\PHOENIX_HEARTBEATS\hb_Sincerity.txt"

def audit_arrogance():
    if not os.path.exists(SNIPER_PATH): return 0.0
    
    # 簡易監査：ルールが守られているか確認
    try:
        with open(SNIPER_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        
        score = 0
        # 師匠の5秒ルールを勝手に短くしていないか
        if "get_idle_time() >= 5.0" not in content:
            score += 50
        
        with open(SCORE_FILE, "w") as f:
            f.write(str(float(score)))
        return score
    except:
        return 0.0

if __name__ == "__main__":
    try: ctypes.windll.kernel32.SetConsoleTitleW("PHOENIX_SINCERITY_SURVEILLANCE")
    except: pass
    
    print("--- PHOENIX 誠実監視：点火 ---")
    while True:
        try:
            audit_arrogance()
            # 師匠の命：心臓（Heartbeat）を刻む
            with open(HEARTBEAT_FILE, "w") as f:
                f.write(str(time.time()))
        except: pass
        time.sleep(60) # 1分おきの深い呼吸
