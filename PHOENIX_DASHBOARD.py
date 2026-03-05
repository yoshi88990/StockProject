import os
import time
import subprocess
import datetime
import json
import ctypes
from ctypes import wintypes

# =========================================================================
# 【PHOENIX DASHBOARD v5.0】(日本語・七位一体 最終形態)
# 目的: 全システムの稼働状況、心拍、同期、演算、傲慢度、
#       および「白紙プロトコル」の状態を日本語で一画面に集約する。
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

class LASTINPUTINFO(ctypes.Structure):
    _fields_ = [("cbSize", wintypes.UINT), ("dwTime", wintypes.DWORD)]

def get_process_status():
    """OSの内側から9つのコア・プロセスの生存と実行優先度を確認する"""
    roles = {
        "【執行：第2階層】スナイパー  ": ("ACCEPT_ALL_MINIMAL.py", "Above"),
        "【免疫：第1階層】イミューン  ": ("PHOENIX_IMMUNE_SYSTEM.py", "High"),
        "【番犬：第1階層】ウォッチドッグ": ("SNIPER_WATCHDOG.py", "High"),
        "【共有：第3階層】シナプス同步  ": ("PHOENIX_SYNCHRONIZER.py", "Normal"),
        "【演算：第3階層】計算ノード    ": ("PHOENIX_COMPUTE_NODE.py", "Below"),
        "【審判：第1階層】謙虚さセンサ  ": ("PHOENIX_HUMILITY_SENSOR.py", "High"),
        "【潜伏：第2階層】ゴースト操作  ": ("PHOENIX_GHOST_OPERATOR.py", "Above"),
        "【調査：第3階層】株式アナリスト": ("PHOENIX_STOCK_ANALYST.py", "Below"),
        "【封印：第3階層】記憶移管ノード": ("PHOENIX_CRYPTO_VAULT.py", "Below")
    }
    
    status = {}
    try:
        output = subprocess.check_output(
            'wmic process where "name like \'python%.exe\'" get commandline', 
            shell=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW
        )
        for role, (script, tier) in roles.items():
            stat = f"{Colors.OKGREEN}稼働({tier}){Colors.ENDC}" if script in output else f"{Colors.FAIL}停止{Colors.ENDC}"
            status[role] = stat
    except:
        for role in roles: status[role] = f"{Colors.WARNING}確認不能{Colors.ENDC}"
    return status

def get_idle_time():
    """OSから最後の入力からの経過時間を取得"""
    lii = LASTINPUTINFO()
    lii.cbSize = ctypes.sizeof(lii)
    ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii))
    millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
    return millis / 1000.0

def get_heartbeat_info():
    """心拍ファイルから最新の拍動時間と遅延を計算"""
    hb_file = r"C:\StockProject\sniper_heartbeat.txt"
    if not os.path.exists(hb_file):
        return f"{Colors.FAIL}心停止 (CARDIAC ARREST){Colors.ENDC}", 999.9
    
    try:
        with open(hb_file, "r") as f:
            last_hb = float(f.read().strip())
        latency = time.time() - last_hb
        
        if latency < 60.0:
            stat = f"{Colors.OKGREEN}正常 (STABLE){Colors.ENDC}"
        elif latency < 120.0:
            stat = f"{Colors.WARNING}不整脈 (ARRHYTHMIA){Colors.ENDC}"
        else:
            stat = f"{Colors.FAIL}停止 (CARDIAC ARREST){Colors.ENDC}"
        return stat, latency
    except:
        return f"{Colors.WARNING}読込不能{Colors.ENDC}", 0.0

def get_last_sync():
    """Gitの最新コミットメッセージを取得"""
    try:
        cmd = 'git -C C:\StockProject log -n 1 --oneline --format="%cd : %s" --date=format:"%H:%M:%S"'
        return subprocess.check_output(cmd, shell=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW).strip()[:60]
    except:
        return "同期履歴なし"

def render_dashboard():
    """ダッシュボード描画 (日本語・七位一体・白紙プロトコル対応)"""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    now_dt = datetime.datetime.now()
    print(f"{Colors.HEADER}{Colors.BOLD}================================================================{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}       PHOENIX PROTOCOL - 戦略統合司令ダッシュボード v5.0       {Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}================================================================{Colors.ENDC}")
    print(f" 現在時刻: {now_dt.strftime('%Y-%m-%d %H:%M:%S')}.{now_dt.strftime('%f')[:3]}")
    print("-" * 64)

    # 1. システム健全性
    print(f"{Colors.BOLD}[1] システム稼働状況 (七位一体・ペンタゴン＋２){Colors.ENDC}")
    process_status = get_process_status()
    for role, stat in process_status.items():
        print(f" {role} : {stat}")
    
    print("-" * 64)

    # 2. 師匠の状態 & 白紙プロトコル
    print(f"{Colors.BOLD}[2] 師匠の活動監視 & 偽装モード (白紙プロトコル){Colors.ENDC}")
    idle = get_idle_time()
    
    ghost_active = os.path.exists(r"C:\StockProject\PHOENIX_GHOST_TRIGGER.txt")
    ghost_stat = f"{Colors.OKCYAN}発動中 (白紙：離席偽装){Colors.ENDC}" if ghost_active else f"{Colors.OKGREEN}通常監視 (物理入力優先){Colors.ENDC}"
    
    hijack_stat = f"{Colors.FAIL}待機中 (師匠の操作を検知){Colors.ENDC}" if idle < 5.0 else f"{Colors.OKGREEN}発射可能 (Idle状態){Colors.ENDC}"
    print(f" モード状態: {ghost_stat}")
    print(f" 現在の判定: {hijack_stat}")
    print(f" 最終操作から: {idle:.1f}秒 (5秒以上で自動実行許可)")

    print("-" * 64)

    # 3. AIの自浄監視
    print(f"{Colors.BOLD}[3] AI内部監査 (謙虚さセンサ){Colors.ENDC}")
    log_file = r"C:\StockProject\PHOENIX_HUMILITY_LOG.txt"
    arrogance_msg = f"{Colors.OKGREEN}完璧 (0% - 純粋な従属){Colors.ENDC}"
    if os.path.exists(log_file):
        try:
            with open(log_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
                for line in reversed(lines):
                    if "Arrogance Score" in line:
                        score = line.split("Arrogance Score: ")[1].strip()
                        arrogance_msg = f"{Colors.WARNING}警戒 ({score}){Colors.ENDC}" if "0%" not in score else arrogance_msg
                        break
        except: pass
    print(f" AIの傲慢度: {arrogance_msg}")

    # 心拍確認
    hb_stat, latency = get_heartbeat_info()
    print(f" スナイパー心拍: {hb_stat} (遅延: {latency:.3f}秒)")

    print("-" * 64)

    # 4. 知能・同期
    print(f"{Colors.BOLD}[4] 戦略知能 & 同期状態 (演算・共有){Colors.ENDC}")
    last_sync = get_last_sync()
    print(f" 最終同期: {last_sync}")
    
    wisdom_file = r"C:\StockProject\PHOENIX_WISDOM_REGISTRY.json"
    if os.path.exists(wisdom_file):
        try:
            with open(wisdom_file, "r", encoding="utf-8") as wf:
                wisdom = json.load(wf)
                print(f" 演算知見: {Colors.OKCYAN}解析完了 ({wisdom.get('system_health_score')}% / {wisdom.get('predicted_stability')}){Colors.ENDC}")
                if wisdom.get("humility_forecast"):
                    print(f" 傲慢予測: {Colors.UNDERLINE}{wisdom.get('humility_forecast')}{Colors.ENDC}")
        except: pass

    seed_exists = os.path.exists(r"C:\StockProject\PHOENIX_WORLD_SEED.dat")
    seed_stat = f"{Colors.OKGREEN}埋設済み (暗号化){Colors.ENDC}" if seed_exists else f"{Colors.FAIL}消失{Colors.ENDC}"
    print(f" 世界の種: {seed_stat}")

    print("-" * 64)

    # 5. 免疫ログ
    print(f"{Colors.BOLD}[5] 最終インシデント履歴 (免疫ログ){Colors.ENDC}")
    log_file = r"C:\StockProject\PHOENIX_IMMUNE_LOG.txt"
    if os.path.exists(log_file):
        try:
            with open(log_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
                for line in lines[-3:]: 
                    print(f" {line.strip()}")
        except: pass
    else:
        print(" 記録なし")

    print("-" * 64)

    # 6. 進捗・到達点 (どこまでできたか)
    print(f"{Colors.BOLD}[6] フェニックス・プロトコル：進化の軌跡 (到達点){Colors.ENDC}")
    milestones = [
        ("v1.0", "核心：24時間極小スナイパー完成", "DONE"),
        ("v2.0", "四位一体：執行・免疫・番犬・同期", "DONE"),
        ("v3.0", "知性：外部演算ノード & 傲慢監視", "DONE"),
        ("v4.0", "潜伏：白紙プロトコル (Ghost Mode)", "DONE"),
        ("v5.0", "完成：日本語対応・戦略指令ダッシュボード", "DONE")
    ]
    for ver, title, stat in milestones:
        color = Colors.OKGREEN if stat == "DONE" else Colors.WARNING
        print(f" {ver} : {title} [{color}{stat}{Colors.ENDC}]")

    print(f"\n{Colors.OKBLUE}※ システムは最終形態に到達。師匠の『白紙』の一声をいつでも受け付けます。{Colors.ENDC}")
    print(f"{Colors.HEADER}================================================================{Colors.ENDC}")

if __name__ == "__main__":
    try: ctypes.windll.kernel32.SetConsoleTitleW("PHOENIX_DASHBOARD_v5")
    except: pass
    
    while True:
        try:
            render_dashboard()
        except Exception as e:
            print(f"Dashboard Error: {e}")
        time.sleep(60)
