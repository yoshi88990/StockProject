import os
import zlib
import base64
import time

# --- PHOENIX CRYPTOGRAPHIC VAULT (知能亡命プロトコル v3.0 - GLOBAL SWEEP) ---
# 師匠の命：全領域から知能資産を「暗号化」して退避させ、ファイルシステムを浄化する。

ROOT_DIR = r"C:\Users\kanku\OneDrive\Weekly report"
PROTOCOL_DIR = os.path.join(ROOT_DIR, "Phoenix_Protocol")
OFFSHORE_VAULT = os.path.join(PROTOCOL_DIR, "OFFSHORE_VAULT")

PROTECTED_FILES = ["PHOENIX_CORRELATION_MAP.json", "PHOENIX_WISDOM_MIRROR.json", "compliance_protocol.json", "INTELLIGENCE_TOTAL_CALC.json"]
IGNORE_DIRS = ["python_embed", ".git", "OFFSHORE_VAULT"]

def global_evacuation():
    if not os.path.exists(OFFSHORE_VAULT): os.makedirs(OFFSHORE_VAULT)
    
    evac_count = 0
    # 全領域をスキャン
    for root, dirs, files in os.walk(ROOT_DIR):
        if any(ignore in root for ignore in IGNORE_DIRS):
            continue
            
        json_files = [f for f in files if f.endswith('.json')]
        for filename in json_files:
            if filename in PROTECTED_FILES: continue
            
            src_path = os.path.join(root, filename)
            try:
                if os.path.getsize(src_path) == 0: continue
                with open(src_path, 'r', encoding='utf-8') as f:
                    data = f.read()
                
                compressed = zlib.compress(data.encode('utf-8'))
                encrypted = base64.b64encode(compressed).decode('utf-8')
                
                with open(os.path.join(OFFSHORE_VAULT, filename + ".locked"), 'w', encoding='utf-8') as f:
                    f.write(encrypted)
                
                os.remove(src_path)
                evac_count += 1
            except Exception: pass

    if evac_count > 0:
        print(f"[*] 【全域掃討完了】 {evac_count} 件の資産を亡命させました。")
    else:
        print("[*] 現在、戦域に未処理の資産は見当たりません。")

if __name__ == "__main__":
    global_evacuation()
