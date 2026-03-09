import time
import os
import sys
import datetime
import subprocess
import shutil
import ctypes
import re
import msvcrt
from colorama import init, Fore, Style, Back

# --- PHOENIX SOVEREIGN DASHBOARD v10.5 [沈黙・誠実・資源] ---
# 師匠の命：【3. 狙撃ログ】および【4. 作戦行動記録】を削除。
# 核心プロセスの拍動、謙虚度監査、そしてCドライブ監視のみを誠実に表示。
# 1分周期・静寂潜伏を貫き、師匠の視界を極限までシンプルに保つ。

init(autoreset=True)

# 監視ディレクトリ
BASE_DIR = r"c:\Users\yoshi\OneDrive\Weekly report"
PROTOCOL_DIR = os.path.join(BASE_DIR, "Phoenix_Protocol")
AUDIT_LOG = os.path.join(PROTOCOL_DIR, "DNA_VAULT", "arrogance_audit.log")

def set_premium_font():
    try:
        LF_FACESIZE = 32
        STD_OUTPUT_HANDLE = -11
        class COORD(ctypes.Structure):
            _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]
        class CONSOLE_FONT_INFOEX(ctypes.Structure):
            _fields_ = [("cbSize", ctypes.c_ulong),
                        ("nFont", ctypes.c_ulong),
                        ("dwFontSize", COORD),
                        ("FontFamily", ctypes.c_uint),
                        ("FontWeight", ctypes.c_uint),
                        ("FaceName", ctypes.c_wchar * LF_FACESIZE)]
        handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
        font = CONSOLE_FONT_INFOEX()
        font.cbSize = ctypes.sizeof(CONSOLE_FONT_INFOEX)
        font.nFont = 0
        font.dwFontSize.X = 14
        font.dwFontSize.Y = 24
        font.FaceName = "MS Gothic"
        ctypes.windll.kernel32.SetCurrentConsoleFontEx(handle, 0, ctypes.byref(font))
    except: pass

def silent_submergence():
    """窓を安定させ、タイトルを設定する（勝手な移動や最小化を禁ずる）。"""
    try:
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        ctypes.windll.kernel32.SetConsoleTitleW("PHOENIX DASHBOARD v10.6 - STABLE")
        # 師匠の命：勝手に最小化(6)したり再配置したりすることを禁ずる。
        # ctypes.windll.user32.ShowWindow(hwnd, 6) 
    except: pass

def get_process_status():
    try:
        # CREATE_NO_WINDOW (0x08000000) でポップアップを完全阻止
        cmd = 'wmic process get commandline'
        output = subprocess.check_output(cmd, shell=True, creationflags=0x08000000, timeout=3.0).decode('cp932', errors='ignore').lower()
        return {
            "Sniper": "accept_all_minimal" in output,
            "Watchdog": "sniper_watchdog" in output,
            "Humility": "humility_sensor" in output,
            "Commander": "commander.py" in output,
            "Receptor": "receptor" in output or "synapse" in output
        }
    except: return {}

def get_disk_status():
    try:
        total, used, free = shutil.disk_usage("C:")
        free_gb = free // (2**30)
        return free_gb
    except: return -1

def get_last_lines(path, n=5):
    if not os.path.exists(path): return []
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            lines = [l for l in f.readlines() if l.strip()]
            return [re.sub(r'[^\x00-\x7F\u3000-\u303F\u3040-\u309F\u30A0-\u30FF\uFF00-\uFFEF\u4E00-\u9FAF\s:-]', '', l.strip()) for l in lines[-n:]]
    except: return []

def render_simple_sovereign_ui(procs=None, free_gb=None):
    # clsを使わずカーソルを(0,0)に戻して描画することで、窓のバウンドを防ぐ
    sys.stdout.write('\033[H')
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if procs is None: procs = {}
    if free_gb is None: free_gb = -1

    print(Fore.CYAN + Style.BRIGHT + "┌──────────────────────────────────────────────────────────────────────────────┐")
    print(Fore.CYAN + Style.BRIGHT + f"│   PHOENIX DASHBOARD v10.6 - 【絶対固定・安定更新】           [{now}] │")
    print(Fore.CYAN + Style.BRIGHT + "└──────────────────────────────────────────────────────────────────────────────┘")
    
    # 資源監視 (Resource)
    print(Fore.WHITE + Style.BRIGHT + " 【 0. システム資源 (SYSTEM HEALTH) 】")
    disk_color = Fore.GREEN if free_gb > 20 else (Fore.YELLOW if free_gb > 10 else Fore.RED)
    disk_msg = f"{free_gb} GB" if free_gb >= 0 else "N/A"
    print(f"  > Cドライブ空き容量 : {disk_color}{disk_msg}" + (Fore.RED + " [Critically Low]" if free_gb < 5 else ""))
    
    # 核心プロセス (Core Units)
    print("\n" + Fore.WHITE + Style.BRIGHT + " 【 1. 核心プロセスの拍動 (CORE PULSE) 】")
    def fmt_st(exists): return Fore.GREEN + "● ACTIVE" if exists else Fore.RED + "○ DEAD"
    
    print(f"  狙撃本体 (Sniper)    : {fmt_st(procs.get('Sniper'))}   |   番犬 (Watchdog) : {fmt_st(procs.get('Watchdog'))}")
    print(f"  謙虚監視 (Humility)  : {fmt_st(procs.get('Humility'))}   |   司令 (Commander): {fmt_st(procs.get('Commander'))}")
    print(f"  受容接続 (Receptor)  : {fmt_st(procs.get('Receptor'))}")
    
    # 監査 (Audit)
    print("\n" + Fore.WHITE + Style.BRIGHT + " 【 2. 誠実さの審判 (HUMILITY AUDIT) 】")
    audit = get_last_lines(AUDIT_LOG, 2)
    if audit:
        for a in audit: print(Fore.RED + f"  {a}")
    else:
        print(Fore.GREEN + "  [!] 謙虚度 100% - AIの傲慢は検知されていません")
    
    # シナプス進捗 (BRAIN SYNAPSE)
    print("\n" + Fore.WHITE + Style.BRIGHT + " 【 3. 脳髄シナプス接続状況 (BRAIN SYNAPSE) 】")
    synapse_log = get_last_lines(r"C:\StockProject\synapse_pulse.txt", 2)
    if synapse_log:
        for s in synapse_log: print(Fore.MAGENTA + Style.BRIGHT + f"  {s}")
    else:
        print(Fore.YELLOW + "  [?] シナプス未接続、または待機中...")

    # 四季報読破進捗 (SHIKIHO PROGRESS)
    print("\n" + Fore.WHITE + Style.BRIGHT + " 【 4. 会社四季報 読破領域 (SHIKIHO PROGRESS) 】")
    shikiho_log_path = r"C:\StockProject\shikiho_progress.txt"
    shikiho_progress = get_last_lines(shikiho_log_path, 4)
    if shikiho_progress:
        for sp in shikiho_progress: print(Fore.BLUE + Style.BRIGHT + f"  [+] {sp}")
    else:
        print(Fore.WHITE + "  [ 解析中 / 待機中 ]")

    # 泥臭さ監視
    print("\n" + Fore.WHITE + Style.BRIGHT + " 【 5. 情報収集の泥臭さ監視 (SCRAPER BEAT) 】")
    heartbeat_path = r"C:\StockProject\scraper_heartbeat.txt"
    try:
        with open(heartbeat_path, "r") as f:
            last_beat = float(f.read().strip())
        diff = time.time() - last_beat
        if diff < 10.0:
            print(Fore.GREEN + Style.BRIGHT + f"  [+] 状況: 脳は生きている。不眠不休で情報収集中 (最終拍動: {diff:.1f}s前)")
        else:
            print(Fore.RED + Style.BRIGHT + f"  [-] 警告: 停滞またはサボり検知 (最終拍動: {diff:.1f}s前)")
    except:
        print(Fore.YELLOW + "  [?] Scraper 未稼働")

    print("\n" + Fore.CYAN + Style.BRIGHT + "────────────────────────────────────────────────────────────────────────────────")
    print(Fore.RED + Style.BRIGHT + " 🚨 【 K 】キー：スナイパー部隊(ACCEPT_ALL)のみを即座に葬る(KILL) 🚨")

if __name__ == "__main__":
    silent_submergence()
    os.system('cls')
    last_wmic_time = 0
    procs_cache = {}
    free_gb_cache = -1

    while True:
        try:
            current_time = time.time()
            if current_time - last_wmic_time > 10:
                procs_cache = get_process_status()
                free_gb_cache = get_disk_status()
                last_wmic_time = current_time
            
            render_simple_sovereign_ui(procs_cache, free_gb_cache)

            # 待機ループ中のキー監視
            for _ in range(300):
                if msvcrt.kbhit():
                    key = msvcrt.getch()
                    if key.lower() == b'k':
                        subprocess.run('taskkill /F /FI "COMMANDLINE eq *ACCEPT_ALL_MINIMAL.py*" /T', shell=True, creationflags=0x08000000)
                        subprocess.run('taskkill /F /FI "COMMANDLINE eq *SNIPER_WATCHDOG.py*" /T', shell=True, creationflags=0x08000000)
                        procs_cache = get_process_status()
                        render_simple_sovereign_ui(procs_cache, free_gb_cache)
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            break
        except Exception:
            time.sleep(2)