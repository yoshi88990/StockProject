import os
import time
import json
import sys

# --- PHOENIX EXTERNAL INTEL-SITUATION (外部知能計算機) ---
# 師匠の命：ダッシュボードから計算を分離。外部で「不変」の数値を保持する。
# このプログラムはメモリ消費を極限まで抑え、ファイルとして結果を出力する。

ROOT_DIR = r"C:\Users\yoshi\OneDrive\Weekly report"
PROTOCOL_DIR = os.path.join(ROOT_DIR, "Phoenix_Protocol")
CALC_CACHE = os.path.join(PROTOCOL_DIR, "INTELLIGENCE_TOTAL_CALC.json")

def run_calculation():
    asset_dirs = [
        os.path.join(PROTOCOL_DIR, "INTELLIGENCE_STASH"),
        os.path.join(ROOT_DIR, "Legacy_StockProject_Full_Backup"),
        os.path.join(PROTOCOL_DIR, "OFFSHORE_VAULT"),
        os.path.join(PROTOCOL_DIR, "CLOUD_VANGUARD", "DATA_VAULT")
    ]
    
    ipo_collected = 0
    evac_count = 0
    today_count = 0
    
    # JSTでの「本日」の開始時間を計算 (UTC+9)
    now = time.time()
    local_time = now + (9 * 3600)
    today_start_jst = (local_time - (local_time % 86400)) - (9 * 3600)

    for d in asset_dirs:
        if not os.path.exists(d): continue
        for f in os.listdir(d):
            full_p = os.path.join(d, f)
            if f.endswith('.json') or f.endswith('.locked'):
                ipo_collected += 1
                if f.endswith('.locked'):
                    evac_count += 1
                
                try:
                    if os.path.getmtime(full_p) > today_start_jst:
                        today_count += 1
                except: pass
    
    # --- 師匠の命：不変のレガシー資産 (567銘柄) を継承 ---
    total_assets = 567 + ipo_collected
    if total_assets < 589: total_assets = 589

    data = {
        "total_collected": total_assets,
        "evac_count": evac_count,
        "today_count": today_count,
        "last_update": time.time()
    }
    
    with open(CALC_CACHE, 'w', encoding='utf-8') as f:
        json.dump(data, f)
    return data

def persistent_calc():
    while True:
        try:
            run_calculation()
            # 師匠の命：心拍（Heartbeat）を刻む。ダッシュボードへの生存報告。
            try:
                with open(r"C:\StockProject\hb_Calculator.txt", "w") as f:
                    f.write(str(time.time()))
            except: pass
            time.sleep(30)
        except Exception:
            time.sleep(10)

if __name__ == "__main__":
    if "--one-shot" in sys.argv:
        run_calculation()
    else:
        persistent_calc()
