# -*- coding: utf-8 -*-
import os
import time
import json
import sys

# --- PHOENIX EXTERNAL INTEL-SITUATION (螟夜Κ遏･閭ｽ險育ｮ玲ｩ・ ---
# 蟶ｫ蛹縺ｮ蜻ｽ・壹ム繝・す繝･繝懊・繝峨°繧芽ｨ育ｮ励ｒ蛻・屬縲ょ､夜Κ縺ｧ縲御ｸ榊､峨阪・謨ｰ蛟､繧剃ｿ晄戟縺吶ｋ縲・
# 縺薙・繝励Ο繧ｰ繝ｩ繝縺ｯ繝｡繝｢繝ｪ豸郁ｲｻ繧呈･ｵ髯舌∪縺ｧ謚代∴縲√ヵ繧｡繧､繝ｫ縺ｨ縺励※邨先棡繧貞・蜉帙☆繧九・

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
    
    # JST縺ｧ縺ｮ縲梧悽譌･縲阪・髢句ｧ区凾髢薙ｒ險育ｮ・(UTC+9)
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
    
    # --- 蟶ｫ蛹縺ｮ蜻ｽ・壻ｸ榊､峨・繝ｬ繧ｬ繧ｷ繝ｼ雉・肇 (567驫俶氛) 繧堤ｶ呎価 ---
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
            # 蟶ｫ蛹縺ｮ蜻ｽ・壼ｿ・牛・・eartbeat・峨ｒ蛻ｻ繧縲ゅム繝・す繝･繝懊・繝峨∈縺ｮ逕溷ｭ伜ｱ蜻翫・
            try:
                with open(HEARTBEAT_FILE, "w") as f:
                    f.write(str(time.time()))
            except: pass
            time.sleep(60) # 10遘帝俣髫・
        except Exception:
            time.sleep(60)

if __name__ == "__main__":
    if "--one-shot" in sys.argv:
        run_calculation()
    else:
        persistent_calc()
