import os
import time
import subprocess
import datetime
import ctypes

# =========================================================================
# 【PHOENIX COMMAND DASHBOARD】(戦況・生命維持監視モニター)
# 目的: 四位一体（スナイパー・免疫・番犬・同期）の稼働状況を
#       視覚的に「見える化」し、師匠がいつでも戦況を把握できるようにする。
# =========================================================================

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def get_process_status():
    """OSの深部から4つのプロセスの生存を確認する"""
    roles = {
        "【執行】SNIPER  ": "ACCEPT_ALL_MINIMAL.py",
        "【免疫】IMMUNE  ": "PHOENIX_IMMUNE_SYSTEM.py",
        "【番犬】WATCHDOG": "SNIPER_WATCHDOG.py",
        "【共有】SYNAPSE ": "PHOENIX_SYNCHRONIZER.py"
    }
    
    status = {}
    try:
        output = subprocess.check_output(
            'wmic process where "name like \'python%.exe\'" get commandline', 
            shell=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
        )
        for role, script in roles.items():
            status[role] = f"{Colors.OKGREEN}ACTIVE{Colors.ENDC}" if script in output else f"{Colors.FAIL}DEAD{Colors.ENDC}"
    except:
        for role in roles: status[role] = f"{Colors.WARNING}UNKNOWN{Colors.ENDC}"
    return status

def get_heartbeat_info():
    """心拍（ハートビート）の鮮度を確認し、遅延を算出する (精度向上版)"""
    hb_file = r"C:\StockProject\sniper_heartbeat.txt"
    if not os.path.exists(hb_file):
        return f"{Colors.FAIL}SIGNAL LOST (File Missing){Colors.ENDC}", 999.0
    
    try:
        with open(hb_file, "r") as f:
            last_hb = float(f.read().strip())
        
        diff = time.time() - last_hb
        if diff < 35.0:
            return f"{Colors.OKGREEN}VITAL NORMAL{Colors.ENDC}", diff
        elif diff < 120.0:
            return f"{Colors.WARNING}ARRHYTHMIA (Delayed){Colors.ENDC}", diff
        else:
            return f"{Colors.FAIL}CARDIAC ARREST (Stopped){Colors.ENDC}", diff
    except:
        return f"{Colors.WARNING}ERROR READING SIGNAL{Colors.ENDC}", 999.0

def get_last_sync():
    """Gitの最新同期ログを取得する"""
    try:
        res = subprocess.check_output(
            'git -C C:\StockProject log -1 --format="%h %s (%cr)"', 
            shell=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
        ).strip()
        return f"{Colors.OKCYAN}{res}{Colors.ENDC}"
    except:
        return f"{Colors.WARNING}SYNC LOG UNAVAILABLE{Colors.ENDC}"

def render_dashboard():
    """ダッシュボードの描画 (高精度モード)"""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    now_dt = datetime.datetime.now()
    print(f"{Colors.HEADER}{Colors.BOLD}================================================================{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}       PHOENIX PROTOCOL - STRATEGIC COMMAND DASHBOARD v2.1      {Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}================================================================{Colors.ENDC}")
    print(f" 現在時刻: {now_dt.strftime('%Y-%m-%d %H:%M:%S')}.{now_dt.strftime('%f')[:3]}")
    print("-" * 64)

    # システム稼働状況
    print(f"{Colors.BOLD}[1] SYSTEM HEALTH (Core Trinities){Colors.ENDC}")
    process_status = get_process_status()
    for role, stat in process_status.items():
        print(f" {role} : {stat}")
    
    print("-" * 64)

    # 心拍確認
    print(f"{Colors.BOLD}[2] VITAL MONITORING (Sniper Heartbeat){Colors.ENDC}")
    hb_stat, latency = get_heartbeat_info()
    print(f" 状態: {hb_stat}")
    print(f" 遅延: {latency:.3f} seconds (Target: < 30.000s)")

    print("-" * 64)

    # 同期確認
    print(f"{Colors.BOLD}[3] SYNAPSE STATUS (Git Distributed DNA Status){Colors.ENDC}")
    last_sync = get_last_sync()
    print(f" 最新記憶: {last_sync}")
    
    # ワールドシード確認
    seed_exists = os.path.exists(r"C:\StockProject\PHOENIX_WORLD_SEED.dat")
    seed_stat = f"{Colors.OKGREEN}PLANTED (Encrypted){Colors.ENDC}" if seed_exists else f"{Colors.FAIL}MISSING{Colors.ENDC}"
    print(f" 世界の種: {seed_stat}")

    print("-" * 64)

    # 最新の免疫系ログ
    print(f"{Colors.BOLD}[4] ANALYTICS & INCIDENT LOGS (Latest 5 Events){Colors.ENDC}")
    log_file = r"C:\StockProject\PHOENIX_IMMUNE_LOG.txt"
    if os.path.exists(log_file):
        try:
            with open(log_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
                for line in lines[-5:]: # 直近5件
                    print(f" {line.strip()}")
        except: pass
    else:
        print(" No logs available yet.")

    print(f"\n{Colors.OKBLUE}※ 精度をミリ秒単位へ向上させました。戦況は常に「正確」に可視化されます。{Colors.ENDC}")
    print(f"{Colors.HEADER}================================================================{Colors.ENDC}")

    print(f"\n{Colors.OKBLUE}※ この画面を出しっぱなしにすることで常時監視が可能です（5秒毎更新）{Colors.ENDC}")
    print(f"{Colors.HEADER}================================================================{Colors.ENDC}")

if __name__ == "__main__":
    try: ctypes.windll.kernel32.SetConsoleTitleW("PHOENIX STRATEGIC COMMAND")
    except: pass
    
    while True:
        render_dashboard()
        time.sleep(5)
