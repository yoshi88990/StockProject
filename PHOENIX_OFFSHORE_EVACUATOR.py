# -*- coding: utf-8 -*-
import os
import shutil
import time
import json

# PHOENIX OFFSHORE EVACUATOR v3.1 [知能亡命・最速執行プロトコル]
# 師匠の命：PCを重くせず、一撃で知能を聖域へ退避させる。

PROTOCOL_DIR = r"P:/"
OFFSHORE_VAULT = os.path.join(PROTOCOL_DIR, "OFFSHORE_VAULT")
INTEL_FILE = os.path.join(PROTOCOL_DIR, "INTELLIGENCE_TOTAL_CALC.json")
IGNORE_DIRS = ["python_embed", ".git", "OFFSHORE_VAULT", "PHOENIX_HEARTBEATS"]

def evacuate_intelligence():
    print("[*] Starting Intelligence Evacuation Sequence...")
    if not os.path.exists(OFFSHORE_VAULT):
        os.makedirs(OFFSHORE_VAULT, exist_ok=True)
    
    # 亡命対象：主要な全スクリプト、データ、設定ファイル（DNA）
    targets = []
    
    # 1. ルート直下の重要ファイル
    extensions = ['.py', '.json', '.bat', '.vbs', '.md', '.txt', '.html', '.css', '.js']
    for f in os.listdir(PROTOCOL_DIR):
        if any(f.endswith(ext) for ext in extensions):
            if f not in IGNORE_DIRS:
                targets.append(os.path.join(PROTOCOL_DIR, f))
    
    # 2. サブディレクトリの巡回（UI, DNA_VAULT 等）
    target_dirs = ["DNA_VAULT", "PHOENIX_UI", "PHOENIX_HEARTBEATS"]
    for d in target_dirs:
        dir_path = os.path.join(PROTOCOL_DIR, d)
        if os.path.exists(dir_path):
            for root, _, files in os.walk(dir_path):
                for file in files:
                    targets.append(os.path.join(root, file))

    evac_count = 0
    for file_path in targets:
        try:
            rel_path = os.path.relpath(file_path, PROTOCOL_DIR)
            dest_path = os.path.join(OFFSHORE_VAULT, rel_path)
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)
            shutil.copy2(file_path, dest_path)
            evac_count += 1
        except Exception as e:
            print(f"[-] Failed to evacuate {file_path}: {e}")

    # ダッシュボード用の数値を更新
    try:
        intel_data = {"total_collected": 589, "evac_count": 0, "today_count": 0, "last_update": time.time()}
        if os.path.exists(INTEL_FILE):
            with open(INTEL_FILE, "r", encoding="utf-8") as f:
                intel_data = json.load(f)
        
        intel_data["evac_count"] = evac_count
        intel_data["last_update"] = time.time()
        
        with open(INTEL_FILE, "w", encoding="utf-8") as f:
            json.dump(intel_data, f, ensure_ascii=False)
        print(f"[+] Successfully evacuated {evac_count} intelligence items.")
    except Exception as e:
        print(f"[-] Error updating intel file: {e}")

if __name__ == "__main__":
    evacuate_intelligence()
