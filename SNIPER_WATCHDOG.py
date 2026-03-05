import os
import time
import hashlib
import shutil
import ctypes

# ==============================================================================
# 【絶対防壁】 24時間監視システム (SNIPER WATCHDOG)
#
# AI（私）の勝手な条件反射や傲慢なリファクタリング（書き換え）から、
# 過去の泥臭い歴史を持つ純正なスナイパーコードを物理的に護り抜く「番犬」です。
# 1秒たりとも隙を見せず、もしAIが勝手にコードを1文字でも書き換えた瞬間、
# 「DNA_VAULT（絶対金庫）」に保存された初期ファイルから即座に上書きして復元します。
# ==============================================================================

BASE_DIR = r"C:\StockProject"
VAULT_DIR = os.path.join(BASE_DIR, "DNA_VAULT")

# 監視・保護対象（AIによる手出し禁止ファイル）
TARGETS = [
    os.path.join(BASE_DIR, "ACCEPT_ALL_MINIMAL.py"),
    os.path.join(BASE_DIR, "PHOENIX_IMMUNE_SYSTEM.py")
]

def get_hash(filepath):
    """ファイルの改ざんを高精度に検知するためのハッシュ取得"""
    if not os.path.exists(filepath):
        return None
    try:
        with open(filepath, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except:
        return None

def watch():
    os.makedirs(VAULT_DIR, exist_ok=True)
    
    vault_hashes = {}
    
    # 起動時に「今の安全なファイル」を金庫（VAULT）にコピーし、それを正と定義する
    for target in TARGETS:
        filename = os.path.basename(target)
        vault_path = os.path.join(VAULT_DIR, filename + ".locked")
        
        # 既に金庫にある場合はコピーしない（初回の「正」の状態をずっと信じる）
        if not os.path.exists(vault_path) and os.path.exists(target):
            shutil.copy2(target, vault_path)
            
        vault_hashes[target] = {
            "vault_path": vault_path,
            "hash": get_hash(vault_path)
        }

    # 24時間・1秒周期の監視ループ（外部プロセス）
    while True:
        for target, info in vault_hashes.items():
            current_hash = get_hash(target)
            
            # AIが勝手に書き換えた（ハッシュが変わった）、あるいは誤って消した場合
            if current_hash != info["hash"]:
                try:
                    # ただちに金庫からオリジナルのDNAを取り出し、強制的に復元する
                    shutil.copy2(info["vault_path"], target)
                    
                    # 違反記録（監査ログ）を残す
                    log_path = os.path.join(VAULT_DIR, "violation.log")
                    with open(log_path, "a", encoding="utf-8") as lf:
                        lf.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 🚨 異常検知: AIによる {os.path.basename(target)} の不正な書き換え(条件反射)を阻止し、元のコード(DNA)を強制復元しました。\n")
                except:
                    pass
        
        # 1秒間隔でAIの行動を監視し続ける
        time.sleep(1.0)

if __name__ == "__main__":
    try: ctypes.windll.kernel32.SetConsoleTitleW("SNIPER_WATCHDOG_24H")
    except: pass
    watch()
