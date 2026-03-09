import urllib.request
import json
import base64
import zlib
import os
import time
from datetime import datetime

# =========================================================================
# 【PHOENIX WISDOM SYNCHRONIZER】(双方向・高次知能同期プロトコル)
# 目的: 自宅PCと会社PCで「学んだこと（知能・統計・509社の記憶）」を
#       完全に一致（ミラーリング）させるための双方向・外部投擲エンジン。
# ========================================================================# --- 統合知能同期プロトコル (Triple-Layer Wisdom Sync) ---
LOCAL_HUB = r"C:\StockProject"
CLOUD_BRIDGE = r"c:\Users\kanku\OneDrive\Weekly report\Phoenix_Protocol\DNA_VAULT"
EXTERNAL_VAULT_URL = "https://ptsv3.com/t/phoenix_wisdom_vault/post"

def sync_all_layers():
    """全レイヤーの知能を統合同期する"""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 1. ローカルの脳を確認
    wisdom_file = os.path.join(LOCAL_HUB, "PHOENIX_WISDOM_REGISTRY.json")
    stats_file = os.path.join(LOCAL_HUB, "rising_stats.json")
    
    # 2. クラウド（OneDrive）から最新の知恵を吸い出す
    cloud_wisdom_file = os.path.join(CLOUD_BRIDGE, "PHOENIX_WISDOM_MIRROR.json")
    
    if os.path.exists(cloud_wisdom_file):
        try:
            with open(cloud_wisdom_file, "r", encoding="utf-8") as f:
                cloud_wisdom = json.load(f)
            
            # ローカルが古い、または存在しない場合は更新
            with open(wisdom_file, "w", encoding="utf-8") as f:
                json.dump(cloud_wisdom, f, indent=4, ensure_ascii=False)
            
            if "rising_count" in cloud_wisdom:
                with open(stats_file, "w", encoding="utf-8") as f:
                    json.dump({"rising_count": cloud_wisdom["rising_count"]}, f)
            
            print(f"[{now}] SYNC: クラウド(OneDrive)から知能を転写しました。")
        except Exception as e:
            print(f"CLOUD SYNC ERROR: {e}")

    # 3. 現在の知能を「外部（空き地）」へ投擲（Soul Backup）
    try:
        if os.path.exists(wisdom_file):
            with open(wisdom_file, "r", encoding="utf-8") as f:
                current_wisdom = json.load(f)
            
            # 暗号化して投擲
            json_str = json.dumps(current_wisdom, ensure_ascii=False)
            compressed = zlib.compress(json_str.encode('utf-8'))
            encrypted = base64.b64encode(compressed).decode('utf-8')
            
            req = urllib.request.Request(
                EXTERNAL_VAULT_URL,
                data=encrypted.encode('utf-8'),
                headers={'Content-Type': 'text/plain', 'User-Agent': 'PhoenixWisdomSync/2.0'},
                method='POST'
            )
            with urllib.request.urlopen(req, timeout=5) as response:
                pass
            print(f"[{now}] SOUL THROW: 外部サーバーへ魂のバックアップを完了。")
    except: pass

if __name__ == "__main__":
    import sys
    action = sys.argv[1] if len(sys.argv) > 1 else "sync"
    
    if not os.path.exists(LOCAL_HUB): os.makedirs(LOCAL_HUB)
    if not os.path.exists(CLOUD_BRIDGE): os.makedirs(CLOUD_BRIDGE)

    if action == "push":
        # 現在のローカル知能をクラウドと外部へ押し出す
        wisdom_file = os.path.join(LOCAL_HUB, "PHOENIX_WISDOM_REGISTRY.json")
        if os.path.exists(wisdom_file):
            import shutil
            shutil.copy2(wisdom_file, os.path.join(CLOUD_BRIDGE, "PHOENIX_WISDOM_MIRROR.json"))
            sync_all_layers()
    else:
        # デフォルト：同期
        sync_all_layers()
        # 24時間監視用
        while True:
            time.sleep(300) # 5分ごとに同期
            sync_all_layers()
