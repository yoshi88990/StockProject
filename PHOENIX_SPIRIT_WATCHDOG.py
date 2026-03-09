import subprocess
import time
import os
import sys
import re
import psutil

# =========================================================================
# 【PHOENIX SPIRIT-WATCHDOG v4.8】(軽量・亡霊根絶版)
# 目的: psutilを使用して軽量にプロセスを監視し、多重起動を物理的に根絶。
# =========================================================================

PYTHONW = r"C:\Users\kanku\OneDrive\Weekly report\python_embed\pythonw.exe"
PROTOCOL_DIR = r"P:/"

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
    """psutilを使用して軽量にプロセスリスト（コマンドライン）を取得"""
    try:
        procs = []
        for p in psutil.process_iter(['cmdline', 'pid']):
            try:
                cmdline = " ".join(p.info['cmdline']) if p.info['cmdline'] else ""
                procs.append(cmdline.lower().replace("\\", "/"))
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return "\n".join(procs)
    except:
        return ""

def kill_by_key(key):
    """特定のキーワードを持つプロセスをpsutilで安全かつ高速に削除"""
    my_pid = os.getpid()
    for p in psutil.process_iter(['cmdline', 'pid']):
        try:
            cmdline = " ".join(p.info['cmdline']) if p.info['cmdline'] else ""
            if key.lower() in cmdline.lower().replace("\\", "/") and "spirit_watchdog" not in cmdline.lower():
                if p.info['pid'] != my_pid:
                    p.terminate() # 優しく停止
                    # p.kill() # 師匠の命：必要なら強引に
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

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
