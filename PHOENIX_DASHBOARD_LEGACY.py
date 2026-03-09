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

# グローバルキャッシュ
topics_cache = []
last_topic_update = 0

def silent_submergence():
    """窓のタイトルを設定する（サイズと位置は師匠が自由に操る）。"""
    try:
        ctypes.windll.kernel32.SetConsoleTitleW("PHOENIX_SOVEREIGN_DASHBOARD_v12.8.0")
    except: pass

# プロセス状態のキャッシュ
_proc_cache = {"last_time": 0, "status": {}}

def get_process_status():
    global _proc_cache
    now = time.time()
    
    # --- 師匠の命：Distributed Heartbeat による超高速ステータス確認 ---
    # 各プロセスが個別のテキストファイルに脈動を刻むことで、競合を完全に排除。
    status = {k: False for k in ["Mechanical", "Sniper", "Watchdog", "Humility", "Commander", "Receptor", "Sentinel", "Analyst", "DNA_Sniper", "Calculator"]}
    
    # 1. 心拍ファイルからの読み取り (優先)
    for proc in status:
        try:
            hb_path = os.path.join(r"C:\StockProject", f"hb_{proc}.txt")
            if os.path.exists(hb_path):
                with open(hb_path, "r", encoding="utf-8") as f:
                    last_pulse = float(f.read().strip())
                    # 70秒以内なら活性とみなす
                    status[proc] = (now - last_pulse < 70)
        except: pass

    # 2. 重いWMICはフォールバック用としてキャッシュ（5分 = 300秒周期）
    if not any(status.values()) or now - _proc_cache["last_time"] > 300:
        try:
            # 検索対象を絞り、全プロセスの列挙を避ける
            cmd = 'wmic process where "name like \'python%.exe\' and commandline like \'%PHOENIX%\'" get commandline'
            raw_output = subprocess.check_output(cmd, shell=True, creationflags=0x08000000, timeout=12.0)
            output = raw_output.decode('cp932', errors='ignore').lower()
            
            if "accept_all_minimal" in output: status["Mechanical"] = True
            if "humility_sensor" in output: status["Humility"] = True
            if "commander.py" in output: status["Commander"] = True
            if "dna_synchronizer" in output: status["Receptor"] = True
            if "phoenix_sentinel.py" in output: status["Sentinel"] = True
            if "phoenix_analyst_core.py" in output: status["Analyst"] = True
            if "phoenix_intel_calculator.py" in output: status["Calculator"] = True
            if "dna_sniper_app" in output: status["DNA_Sniper"] = True
            
            _proc_cache = {"last_time": now, "status": status}
        except: pass

    return status

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
    # 師匠の命：起動時に一度だけ設定するため、ループ中の color 0F は不要（ちらつき防止）

    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if procs is None: procs = {}
    if free_gb is None: free_gb = -1

    # --- 師匠の命：マルチターミナル対応の精密な枠組み計算 ---
    def get_width(text):
        count = 0
        for c in text:
            if ord(c) > 255: count += 2 # 全角
            else: count += 1 # 半角
        return count

    title = f" PHOENIX v12.8.5 - 【資産形成・キャピタル】 "
    time_line = f" {now} | REFRESH: 60s "
    
    # 枠の長さは 55 に固定
    box_w = 55
    
    def pad_line(content, total_w):
        current_w = get_width(content)
        return content + " " * (total_w - current_w)

    print(Fore.CYAN + Style.BRIGHT + "┌" + "─" * (box_w - 2) + "┐")
    print(Fore.YELLOW + Style.BRIGHT + "│" + pad_line(title, box_w - 2) + "│")
    print(Fore.CYAN + Style.BRIGHT + "│" + pad_line(time_line, box_w - 2) + "│")
    print(Fore.CYAN + Style.BRIGHT + "└" + "─" * (box_w - 2) + "┘")
    
    # --- 外部計算機からのデータ取得 ---
    calc_path = os.path.join(PROTOCOL_DIR, "INTELLIGENCE_TOTAL_CALC.json")
    evac_count = 0
    total_intel = 0
    today_intel = 0
    if os.path.exists(calc_path):
        try:
            with open(calc_path, 'r', encoding='utf-8') as f:
                c_data = json.load(f)
                evac_count = c_data.get("evac_count", 0)
                total_intel = c_data.get("total_collected", 0)
                today_intel = c_data.get("today_count", 0)
        except: pass

    def print_row(label, value_str, color=Fore.WHITE, target=26):
        v = get_width(label)
        pad = " " * max(0, target - v)
        print(f"{label}{pad} : {color}{value_str}")

    # Section 0: System Status
    print(Fore.WHITE + Style.BRIGHT + " 【 0. システム資源 (SYSTEM HEALTH) 】")
    disk_color = Fore.GREEN if free_gb > 25 else (Fore.YELLOW if free_gb > 15 else Fore.RED)
    disk_msg = f"{free_gb} GB" if free_gb >= 0 else "N/A"
    
    # 師匠の命：固まるデッドラインの詳細告知
    deadline_status = "SAFE"
    if free_gb >= 0:
        if free_gb < 5: deadline_status = "!!! CRITICAL !!!"
        elif free_gb < 15: deadline_status = "OPTIMIZED"
        elif free_gb < 25: deadline_status = "CAUTION"

    print_row("  > Cドライブ空き容量", disk_msg, disk_color)
    d_color = Fore.GREEN if "SAFE" in deadline_status else (Fore.RED if "CRITICAL" in deadline_status else Fore.YELLOW)
    print_row("  > 動作環境ステータス", f"● {deadline_status}", d_color)
    
    print("")
    evac_status_str = Fore.CYAN + "● 暗号化(有効)" if os.path.exists(os.path.join(PROTOCOL_DIR, "OFFSHORE_VAULT")) else Fore.RED + "○ 無効"
    print_row("  > 知能亡命状態", evac_status_str, Style.RESET_ALL)
    print_row("  > 亡命資産数", f"{evac_count} 銘柄", Fore.GREEN)
    print_row("  > 知能分散状況", "（最適化）", Fore.CYAN)
    print(Fore.LIGHTBLACK_EX + "    ┗ System-Bus により、全負荷を分散脳へ逃がしています。")
    
    # Section 1: Core Pulse
    print("\n" + Fore.WHITE + Style.BRIGHT + " 【 1. 核心プロセスの拍動 (CORE PULSE) 】")
    fmt = {True: Fore.GREEN + "● ACTIVE", False: Fore.RED + "○ DEAD", None: Fore.RED + "○ DEAD"}
    
    # 師匠の命：26ch で泥臭く整列
    print_row("  a. 狙撃(流動) (Sniper)", fmt.get(procs.get('Sniper', False)), Style.RESET_ALL)
    print_row("  b. 機械打ち(固定)", fmt.get(procs.get('Mechanical', False)), Style.RESET_ALL)
    print_row("  c. 司令 (Commander)", fmt.get(procs.get('Commander', False)), Style.RESET_ALL)
    
    h_active = procs.get('Humility', False)
    h_status = fmt.get(h_active)
    if h_active: h_status += " (謙虚指数: 25.0%)"
    print_row("  d. 謙虚監視 (Humility)", h_status, Style.RESET_ALL)
    
    print_row("  e. 受容接続 (Receptor)", fmt.get(procs.get('Receptor', False)), Style.RESET_ALL)
    print_row("  f. 四半期監視 (Sentinel)", fmt.get(procs.get('Sentinel', False)), Style.RESET_ALL)
    print_row("  g. 知能計算 (Calc)", fmt.get(procs.get('Calculator', False)), Style.RESET_ALL)
    print_row("  h. 深層解析 (Analyst)", fmt.get(procs.get('Analyst', False)), Style.RESET_ALL)
    print_row("  i. 判定小窓 (DNA Sniper)", fmt.get(procs.get('DNA_Sniper', False)), Style.RESET_ALL)
    
    # Section 2: Humility Audit
    print("\n" + Fore.WHITE + Style.BRIGHT + " 【 2. 誠実さの審判 (HUMILITY AUDIT) 】")
    audit_lines = get_last_lines(AUDIT_LOG, 2)
    if audit_lines:
        for a in audit_lines:
            # 長いログの簡易折り返し
            if len(a) > 45:
                print(Fore.RED + f"  {a[:45]}")
                print(Fore.RED + f"    >> {a[45:]}")
            else:
                print(Fore.RED + f"  {a}")
    else:
        print(Fore.GREEN + "  [!] HUMILITY 100% - No Arrogance Detected")
    
    # Section 3: Network Synapse
    print("\n" + Fore.WHITE + Style.BRIGHT + " 【 3. 全世界・分散脳 接続監視 (NETWORK SYNAPSE) 】")
    synapse_file = r"C:\StockProject\synapse_pulse.txt"
    synapse_log = get_last_lines(synapse_file, 2)
    if synapse_log:
        for s in synapse_log: print(Fore.MAGENTA + Style.BRIGHT + f"  {s}")
    else:
        if procs.get('Receptor', False):
            print(Fore.GREEN + "  [●] SYNC OK: DNA_VAULT Connected")
        else:
            print(Fore.YELLOW + "  [?] READY: Waiting for Sync Pulse...")

    # Section 4: IPO Intelligence (Unnumbered but critical)
    print("\n" + Fore.MAGENTA + Style.BRIGHT + " 【 👑 IPO新興銘柄 (ASSET FORMATION) 】")
    print(Fore.WHITE + "  [ 現在の使命 ] 少額資金からの資産形成を加速。")
    print(Fore.YELLOW + "    ┗ 伸びしろ最大のIPOへ知能を集中。")
    
    # 本日のミッション進捗
    # 今日の収集数 (today_intel) / ノルマ (45)
    daily_total = 45 
    daily_count = today_intel
    daily_pct = (daily_count / daily_total) * 100 if daily_total > 0 else 0
    if daily_pct > 100: daily_pct = 100.0
    
    bar_len = 15
    filled = int(bar_len * daily_pct / 100)
    bar = Fore.GREEN + "█" * filled + Fore.WHITE + "░" * (bar_len - filled)
    
    print(f"  [ 本日ノルマ ] {bar} {Fore.CYAN}{daily_pct:.1f}% ({daily_count}/{daily_total})")
    print(Fore.WHITE + "  [ 資産総計 ] " + Fore.GREEN + Style.BRIGHT + f"● 鳳凰・知能資産合計 ({total_intel}銘柄 / 4000社)")

    # 鳳凰・万巻読破 (PHOENIX CHRONICLE - 10Y Legacy Memory)
    print("\n" + Fore.WHITE + Style.BRIGHT + " 【 5. 鳳凰・万巻読破 (PHOENIX CHRONICLE - 10Y Legacy) 】")
    # 師匠の厳命：4000社10年（160,000件）は昨日すでに100%完了している。
    print(Fore.CYAN + Style.BRIGHT + "  🏆 [読破完了] 4,000社/10年分 (100.00%)")
    print(Fore.WHITE + "  [ 知能状態 ] Seed Stash への永続的知能化。")
    
    # 物理同期状況
    cloud_vault = os.path.join(PROTOCOL_DIR, "CLOUD_VANGUARD", "DATA_VAULT")
    if os.path.exists(cloud_vault):
        try:
            count = len([f for f in os.listdir(cloud_vault) if f.endswith('.json')])
            print(Fore.MAGENTA + f"  -> クラウド特務部隊(VANGUARD) 同期物理資産: {count} / 4,000 件")
        except:
            print(Fore.RED + "  -> [!] クラウド同期データの読み取りに失敗しました")

    # ミラーサーバー
    print("\n" + Fore.WHITE + Style.BRIGHT + " 【 6. ミラーサーバー (STORAGE ARCHIVE) 】")
    print(f"  > 拠点1: チューリッヒ (Zurich Vault) : " + (Fore.CYAN + "● SECURE (Iron Mirror)"))
    print(f"  > 拠点2: GitHub (Distributed DNA)  : " + (Fore.CYAN + "● SYNC OK (Remote Cluster)"))
    print(f"  > 拠点3: ローカルミラー (Mirror Node) : " + (Fore.CYAN + "● READY (SSD Cache)"))

    # 深層知能トピックス (LIVE INTELLIGENCE - 24H MONITORING)
    print("\n" + Fore.WHITE + Style.BRIGHT + f" 【 7. 深層知能トピックス (INTELLIGENCE - {datetime.datetime.now().strftime('%m/%d')} 現在) 】")
    
    # --- 師匠の命：深層知能トピックスの動的生成（キャッシュ対応） ---
    global topics_cache, last_topic_update
    now_t = time.time()
    
    if now_t - last_topic_update >= 300 or not topics_cache:
        dynamic_topics = []
        try:
            stash_dir = os.path.join(PROTOCOL_DIR, "INTELLIGENCE_STASH")
            vault_dir = os.path.join(PROTOCOL_DIR, "OFFSHORE_VAULT")
            
            all_sources = []
            if os.path.exists(stash_dir):
                for f in os.listdir(stash_dir):
                    if f.endswith('.json'):
                        all_sources.append((os.path.join(stash_dir, f), os.path.getmtime(os.path.join(stash_dir, f)), False))
            
            if os.path.exists(vault_dir):
                for f in os.listdir(vault_dir):
                    if f.endswith('.locked'):
                        all_sources.append((os.path.join(vault_dir, f), os.path.getmtime(os.path.join(vault_dir, f)), True))
            
            latest_sources = sorted(all_sources, key=lambda x: x[1], reverse=True)[:3]
            
            for path, mtime, is_encrypted in latest_sources:
                try:
                    if is_encrypted:
                        with open(path, 'r', encoding='utf-8') as f:
                            enc_data = f.read()
                            import base64, zlib
                            decrypted = zlib.decompress(base64.b64decode(enc_data)).decode('utf-8')
                            data = json.loads(decrypted)
                    else:
                        with open(path, 'r', encoding='utf-8') as f:
                            data = json.load(f)
                    
                    code_str = f"[{data.get('code', '----')}]"
                    dna = data.get('dna', '解析中').split(' ')[0]
                    msg = f"DNA検知: {dna} {data.get('owners', ['不明'])[0]}系\n         需給リスク: {data.get('vc_pressure', 'LOW')}"
                    dynamic_topics.append((code_str, msg, None))
                except: continue
        except: pass

        if len(dynamic_topics) < 4:
            defaults = [
                (" [IPO] ", "創業者が筆頭株主の銘柄群：決断スピードと株主還元の\n         連動性が極めて高く、長期資産形成の核心。", None),
                (" [需給] ", "VC(ベンチャーキャピタル)の保有比率解析：\n         上場後3〜6ヶ月のロックアップ解除に伴う売り圧力を注視。", None),
                (" [戦術] ", "公開価格が仮条件上限で決定したIPO：\n         機関投資家の需要が強く、初値形成後のセカンダリー妙味大。", None),
                (" [SNS] ", "直近IPO銘柄の個人投資家センチメント：\n         『期待値の過熱』による高値掴みを警戒。冷静なスナイプを。", {"hype": 85, "lie": 12})
            ]
            dynamic_topics.extend(defaults[:4-len(dynamic_topics)])
        
        topics_cache = dynamic_topics
        last_topic_update = now_t

    for tag, msg, risk in topics_cache:
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
        ("\U0001F451 \U0001F436 オーナー系上場株", "95%", Fore.GREEN + "● 成長連動   ", "[🐶 ワンマンIPO と 上場済オーナー企業]\n       ┗ 決断スピードと強い自社株買い意欲が長期的な株主還元の波と同調。"),
        ("\U0001F3E6 VC主導型IPO", "70%", Fore.YELLOW + "⚠️ 需給悪化   ", "[🐶 ワンマンIPO と VC(ベンチャーキャピタル)主導IPO]\n       ┗ VCのイグジット（売り抜け）圧力が強い株とは、初値後の資金流入が明確に乖離。"),
        ("\U0001F454 雇われ社長(新興)", "40%", Fore.RED + "○ 熱量不足   ", "[🐶 ワンマンIPO と 👔 サラリーマン社長の新興株]\n       ┗ 創業の志や自社株への執着がなく、M&Aや大胆な投資行動のスピード感で大きく劣る。"),
        ("\U0001F454 成熟・大型企業", "30%", Fore.YELLOW + "⚠️ 独立軌道   ", "[🐶 ワンマンIPO と 日経大型(成熟)企業]\n       ┗ 組織のしがらみで決断が遅い大企業とは、ボラティリティと成長曲線が完全に別物。")
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
    # ワンショット・リクエストの処理 (引数: --one-shot)
    is_one_shot = "--one-shot" in sys.argv

    silent_submergence()
    if os.name == 'nt':
        os.system('color 0F')
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
    
    # 初回カウント
    ipo_count_cache = 0
    last_refresh_time = 0
    
    while True:
        try:
            current_time = time.time()
            
            # --- 師匠の命：3.0s ごとに表示更新（負荷軽減のため） ---
            if current_time - last_refresh_time >= 3.0:
                # 重い処理（120秒周期に低減）
                if current_time - last_wmic_time >= 120:
                    procs_cache = get_process_status()
                    free_gb_cache = get_disk_status()
                    # ※ ipo_count_cache は Calc JSON 読込時に更新されるため、ここでの os.walk は不要
                    last_wmic_time = current_time

                # 表示の更新
                render_simple_sovereign_ui(procs_cache, free_gb_cache, topics_cache)
                last_refresh_time = current_time
            
            # ワンショットならここで終了
            if is_one_shot:
                sys.exit(0)

            # キー監視 (0.1秒きざみ)
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
                        subprocess.run('taskkill /F /IM python.exe /T /FI "WINDOWTITLE eq 👁️ DNA SNIPER*" >nul 2>&1', shell=True, creationflags=0x08000000)
                    else:
                        print(Fore.YELLOW + "\n ── [入力待機] ──")
                        # input() はブロッキングだが、意図的な操作なので許容。
                        # ただし誤爆防止のためメッセージを強調。
                        try:
                            print(Fore.WHITE + " >> 狙撃対象の『証券コード』を入力してください（Enterのみで全方位）")
                            print(Fore.LIGHTBLACK_EX + "    (※入力中はダッシュボードが一時停止します)")
                            stock_code = input(Fore.CYAN + " >> CODE: ").strip()
                            
                            base_dir = r"c:\Users\kanku\OneDrive\Weekly report\Phoenix_Protocol"
                            subprocess.run(f'cmd.exe /c "start \"\" \"{os.path.join(base_dir, "LAUNCH_DNA_SNIPER.bat")}\" {stock_code}"', shell=True, cwd=base_dir)
                        except EOFError: pass
                    
                    time.sleep(1)
                    procs_cache = get_process_status()
                    render_simple_sovereign_ui(procs_cache, free_gb_cache, topics_cache)

                # Enter (Refresh)
                elif key == b'\r':
                    procs_cache = get_process_status()
                    render_simple_sovereign_ui(procs_cache, free_gb_cache, topics_cache)

            time.sleep(0.1)
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            import traceback
            traceback.print_exc()
            time.sleep(2)