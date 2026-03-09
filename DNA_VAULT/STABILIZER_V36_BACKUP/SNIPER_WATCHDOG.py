import os
import time
import hashlib
import shutil
import ctypes

# ==============================================================================
# 【絶対防壁】 24時間監視システム (SNIPER WATCHDOG v3.1)
#
# 誠実さと傲慢：AIの傲慢から、師匠の「正解」を物理的に護り抜く。
# ==============================================================================

BASE_DIR = r"C:\Users\yoshi\OneDrive\Weekly report"
PROTOCOL_DIR = os.path.join(BASE_DIR, "Phoenix_Protocol")
VAULT_DIR = os.path.join(PROTOCOL_DIR, "DNA_VAULT")

# 監視・保護対象
TARGETS = [
    os.path.join(PROTOCOL_DIR, "ACCEPT_ALL_MINIMAL.py"),
    os.path.join(PROTOCOL_DIR, "PHOENIX_HUMILITY_SENSOR.py"),
    os.path.join(BASE_DIR, "PHOENIX_REBIRTH.vbs")
]

def get_hash(filepath):
    """ファイルのSHA256ハッシュを計算"""
    if not os.path.exists(filepath): return None
    try:
        with open(filepath, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()
    except: return None

humility_proc = None
def check_arrogance():
    """傲慢センサーを外部プロセスとして起動・維持する"""
    global humility_proc
    try:
        import subprocess
        humility_script = os.path.join(PROTOCOL_DIR, "PHOENIX_HUMILITY_SENSOR.py")
        
        # CPU負荷と画面ポップアップを防ぐため、プロセスIDで直接追跡
        if humility_proc is None or humility_proc.poll() is not None:
            pythonw = r"C:\Users\yoshi\AppData\Local\Python\bin\pythonw.exe"
            humility_proc = subprocess.Popen([pythonw, humility_script], creationflags=subprocess.CREATE_NO_WINDOW)
    except: pass

def watch():
    os.makedirs(VAULT_DIR, exist_ok=True)
    vault_hashes = {}
    
    # 起動時に現在のDNAを正として金庫（VAULT）にロックする
    for target in TARGETS:
        filename = os.path.basename(target)
        vault_path = os.path.join(VAULT_DIR, filename + ".locked")
        if os.path.exists(target):
            shutil.copy2(target, vault_path)
            
        vault_hashes[target] = {
            "vault_path": vault_path,
            "hash": get_hash(vault_path)
        }

    while True:
        # 1. 物理的な書き換え（改ざん）を阻止
        for target, info in vault_hashes.items():
            current_hash = get_hash(target)
            if current_hash != info["hash"]:
                try:
                    shutil.copy2(info["vault_path"], target)
                    log_path = os.path.join(VAULT_DIR, "violation.log")
                    with open(log_path, "a", encoding="utf-8") as lf:
                        lf.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] 🚨 物理改ざん検知: {os.path.basename(target)} をDNA復元。\n")
                except: pass
        
        # 2. 倫理的な暴走（傲慢）を監視
        check_arrogance()
        
        time.sleep(2.0)

if __name__ == "__main__":
    try: ctypes.windll.kernel32.SetConsoleTitleW("PHOENIX_WATCHDOG_V3")
    except: pass
    watch()
