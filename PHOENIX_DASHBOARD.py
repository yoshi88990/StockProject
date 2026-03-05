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

class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]

def get_idle_time():
    """OSから最後に操作があった時間を取得し、待機時間を秒で返す"""
    lii = LASTINPUTINFO()
    lii.cbSize = ctypes.sizeof(lii)
    ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii))
    millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
    return millis / 1000.0

def render_dashboard():
    """ダッシュボードの描画 (五位一体・フルスペクトラム監視モード)"""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    now_dt = datetime.datetime.now()
    print(f"{Colors.HEADER}{Colors.BOLD}================================================================{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}       PHOENIX PROTOCOL - STRATEGIC COMMAND DASHBOARD v2.5      {Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}================================================================{Colors.ENDC}")
    print(f" 現在時刻: {now_dt.strftime('%Y-%m-%d %H:%M:%S')}.{now_dt.strftime('%f')[:3]}")
    print("-" * 64)

    # システム稼働状況
    print(f"{Colors.BOLD}[1] SYSTEM HEALTH (Full Core Trinities + Compute Node){Colors.ENDC}")
    process_status = get_process_status()
    for role, stat in process_status.items():
        print(f" {role} : {stat}")
    
    print("-" * 64)

    # 師匠の操作監視 (Zero Hijack Status)
    print(f"{Colors.BOLD}[2] ZERO HIJACK MONITORING (User Activity){Colors.ENDC}")
    idle = get_idle_time()
    hijack_stat = f"{Colors.FAIL}HOLD (User Active){Colors.ENDC}" if idle < 5.0 else f"{Colors.OKGREEN}READY (Idle){Colors.ENDC}"
    print(f" 師匠の状態: {hijack_stat}")
    print(f" 非操作時間: {idle:.1f}s (5s以上で自動発射許可)")

    print("-" * 64)

    # 心拍確認
    print(f"{Colors.BOLD}[3] VITAL MONITORING (Sniper Heartbeat){Colors.ENDC}")
    hb_stat, latency = get_heartbeat_info()
    print(f" 心肺状態: {hb_stat}")
    print(f" 心拍遅延: {latency:.3f}s")

    print("-" * 64)

    # 同期・演算確認
    print(f"{Colors.BOLD}[4] SYNAPSE & COMPUTE STATUS (Strategic Intelligence){Colors.ENDC}")
    last_sync = get_last_sync()
    print(f" 最新記憶: {last_sync}")
    
    # 演算エンジンの分析結果（Wisdom Registry）を確認
    wisdom_file = r"C:\StockProject\PHOENIX_WISDOM_REGISTRY.json"
    if os.path.exists(wisdom_file):
        try:
            with open(wisdom_file, "r", encoding="utf-8") as wf:
                wisdom = json.load(wf)
                print(f" 演算知見: {Colors.OKCYAN}ANALYSIS {wisdom.get('system_health_score')}% / {wisdom.get('predicted_stability')}{Colors.ENDC}")
        except: pass
    
    # ワールドシード確認
    seed_exists = os.path.exists(r"C:\StockProject\PHOENIX_WORLD_SEED.dat")
    seed_stat = f"{Colors.OKGREEN}PLANTED (Encrypted){Colors.ENDC}" if seed_exists else f"{Colors.FAIL}MISSING{Colors.ENDC}"
    print(f" 世界の種: {seed_stat}")

    print("-" * 64)

    # 最新の免疫系ログ
    print(f"{Colors.BOLD}[5] ANALYTICS & INCIDENT LOGS (Latest 3 Events){Colors.ENDC}")
    log_file = r"C:\StockProject\PHOENIX_IMMUNE_LOG.txt"
    if os.path.exists(log_file):
        try:
            with open(log_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
                for line in lines[-3:]: 
                    print(f" {line.strip()}")
        except: pass
    else:
        print(" No logs available yet.")

    print(f"\n{Colors.OKBLUE}※ 外部演算エンジン（Pre-Compute Node）がOS全域で自律思考を開始しました。{Colors.ENDC}")
    print(f"{Colors.HEADER}================================================================{Colors.ENDC}")

    print(f"\n{Colors.OKBLUE}※ この画面を出しっぱなしにすることで常時監視が可能です（5秒毎更新）{Colors.ENDC}")
    print(f"{Colors.HEADER}================================================================{Colors.ENDC}")

if __name__ == "__main__":
    try: ctypes.windll.kernel32.SetConsoleTitleW("PHOENIX STRATEGIC COMMAND")
    except: pass
    
    while True:
        render_dashboard()
        time.sleep(5)
