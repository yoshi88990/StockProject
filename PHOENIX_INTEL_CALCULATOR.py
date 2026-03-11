# -*- coding: utf-8 -*-
import os
import time
import json
import sys

# --- PHOENIX INTEL CALCULATOR v1.2 [外部知能計算機・資産統計] ---
# 師匠の命：ダッシュボードから計算を分離。外部で「不変」の数値を保持する。
# PCを重くしないよう、60秒に1回、静かに統計を更新する。

PROTOCOL_DIR = r"P:/"
CALC_CACHE = os.path.join(PROTOCOL_DIR, "INTELLIGENCE_TOTAL_CALC.json")
HEARTBEAT_FILE = r"P:\PHOENIX_HEARTBEATS\hb_Calculator.txt"

def run_calculation():
    asset_dirs = [
        os.path.join(PROTOCOL_DIR, "INTELLIGENCE_STASH"),
        os.path.join(PROTOCOL_DIR, "Legacy_StockProject_Full_Backup"),
        os.path.join(PROTOCOL_DIR, "OFFSHORE_VAULT"),
        os.path.join(PROTOCOL_DIR, "CLOUD_VANGUARD", "DATA_VAULT")
    ]
    
    ipo_collected = 0
    evac_count = 0
    today_count = 0
    
    # 師匠の命：本日(JST)の開始時間を計算
    now = time.time()
    local_time = now + (9 * 3600)
    today_start_jst = (local_time - (local_time % 86400)) - (9 * 3600)

    # 1. 資産ディレクトリ全体のカウント
    for d in asset_dirs:
        if not os.path.exists(d): continue
        for root, _, files in os.walk(d):
            for f in files:
                full_p = os.path.join(root, f)
                # 知能ファイルとして計数
                ipo_collected += 1
                
                # 亡命先(OFFSHORE_VAULT)にあるものはすべて亡命成功数とする
                if "OFFSHORE_VAULT" in root:
                    evac_count += 1
                
                try:
                    if os.path.getmtime(full_p) > today_start_jst:
                        today_count += 1
                except: pass
    
    # 師匠の命：レガシー資産 (589銘柄の魂) をベースにする
    total_assets = max(589, ipo_collected)

    data = {
        "total_collected": total_assets,
        "evac_count": evac_count,
        "today_count": today_count,
        "last_update": time.time()
    }
    
    with open(CALC_CACHE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    return data

def persistent_calc():
    print("--- PHOENIX CALC: 資産統計・開始 ---")
    while True:
        try:
            run_calculation()
            # 師匠の命：心臓（Heartbeat）を刻む
            with open(HEARTBEAT_FILE, "w") as f:
                f.write(str(time.time()))
        except Exception as e:
            print(f"Calc error: {e}")
        time.sleep(60)

if __name__ == "__main__":
    if "--one-shot" in sys.argv:
        run_calculation()
    else:
        persistent_calc()
