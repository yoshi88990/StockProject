import subprocess
import time
import os
import sys
import re

# =========================================================================
# 【PHOENIX SPIRIT-WATCHDOG v4.5】(亡霊根絶・一極集中版)
# 目的: 重複プロセスを検知し、多重起動（亡霊）を完全に消去して一貫性を保つ。
# =========================================================================

PYTHONW = r"C:\Users\kanku\OneDrive\Weekly report\python_embed\pythonw.exe"
PROTOCOL_DIR = r"P:\"

TARGETS = [
    {"name": "b. 機械打ち", "script": os.path.join(PROTOCOL_DIR, "ACCEPT_ALL_MINIMAL.py"), "key": "ACCEPT_ALL_MINIMAL.py"},
    {"name": "c. 司令", "script": os.path.join(PROTOCOL_DIR, "commander.py"), "key": "commander.py"},
    {"name": "d. 謙虚監視", "script": os.path.join(PROTOCOL_DIR, "PHOENIX_HUMILITY_SENSOR.py"), "key": "PHOENIX_HUMILITY_SENSOR.py"},
    {"name": "e. 受容接続", "script": os.path.join(PROTOCOL_DIR, "PHOENIX_DNA_SYNCHRONIZER.py"), "key": "PHOENIX_DNA_SYNCHRONIZER.py"},
    {"name": "f. 四半期監視", "script": os.path.join(PROTOCOL_DIR, "PHOENIX_SENTINEL.py"), "key": "PHOENIX_SENTINEL.py"},
    {"name": "g. 深層解析", "script": os.path.join(PROTOCOL_DIR, "PHOENIX_ANALYST_CORE.py"), "key": "PHOENIX_ANALYST_CORE.py"}
]

LOG_FILE = os.path.join(PROTOCOL_DIR, "spirit_watchdog.log")

def log_res(msg):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")

def get_running_processes():
    try:
        # WMICでコマンドラインを取得。null文字を除去しデコード
        cmd = 'wmic process where "name like \'python%.exe\'" get commandline,processid'
        output = subprocess.check_output(cmd, shell=True, creationflags=0x08000000)
        return output.replace(b'\x00', b'').decode('cp932', errors='ignore').lower().replace("\\", "/")
    except:
        return ""

def kill_by_key(key):
    """特定のキーワードを持つPythonプロセスを、このWatchdog自身を除いて全削除"""
    try:
        cmd = 'wmic process where "name like \'python%.exe\'" get commandline,processid'
        raw = subprocess.check_output(cmd, shell=True, creationflags=0x08000000)
        lines = raw.replace(b'\x00', b'').decode('cp932', errors='ignore').lower().replace("\\", "/").splitlines()
        
        my_pid = os.getpid()
        for line in lines:
            if key.lower() in line and "spirit_watchdog" not in line:
                parts = line.strip().split()
                if parts:
                    pid = parts[-1] 
                    if pid.isdigit() and int(pid) != my_pid:
                        subprocess.run(f"taskkill /F /PID {pid}", shell=True, creationflags=0x08000000)
    except:
        pass

def check_and_stabilize():
    processes = get_running_processes()
    
    for target in TARGETS:
        t_key = target["key"].lower()
        # プロセスリスト内に出現する回数を数える
        count = processes.count(t_key)
        
        if count == 0:
            log_res(f"⚠️ {target['name']} 消失を確認。蘇生します。")
            subprocess.Popen([PYTHONW, target["script"]], creationflags=0x00000008 | 0x08000000)
        elif count > 1:
            log_res(f"🚨 {target['name']} の増殖（{count}件）を検知。根絶し、単一化します。")
            kill_by_key(t_key)
            time.sleep(1)
            subprocess.Popen([PYTHONW, target["script"]], creationflags=0x00000008 | 0x08000000)
            log_res(f"  -> {target['name']} をクリーンな状態で再展開しました。")
        # count == 1 の場合は正常（静止）

    # --- 積極的亡命実行 (60秒周期) ---
    global last_evacuation_time
    if time.time() - last_evacuation_time >= 60:
        evacuator = os.path.join(PROTOCOL_DIR, "PHOENIX_OFFSHORE_EVACUATOR.py")
        if os.path.exists(evacuator):
            subprocess.run([r"C:\Users\kanku\OneDrive\Weekly report\python_embed\python.exe", evacuator], creationflags=0x08000000)
            last_evacuation_time = time.time()

if __name__ == "__main__":
    import ctypes
    try: ctypes.windll.kernel32.SetConsoleTitleW("PHOENIX_WATCHDOG_v4.8_IRON_WILL")
    except: pass

    last_evacuation_time = 0 # 初回実行用

    print("=================================================================")
    print("【PHOENIX SPIRIT-WATCHDOG v4.6】IRON_WILL 起動。")
    print(" 1. プロセスの「増殖」を自動検知し、多重起動を物理的に根絶。")
    print(" 2. 知能資産の「自動暗号化・亡命」を1時間毎に実行。")
    print("=================================================================")

    while True:
        try:
            check_and_stabilize()
        except:
            pass
        time.sleep(10) # 10秒に一度の精密検査（CPU負荷軽減）
