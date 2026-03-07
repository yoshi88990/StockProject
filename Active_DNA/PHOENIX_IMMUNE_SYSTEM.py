import subprocess
import time
import datetime
import os
import sys

# --- PHOENIX IMMUNE SYSTEM (謙虚・監視・遍在) V3.7 ---
# どこでも動く(Portable)ように、絶対パスを廃止。自律的に自分と脳(Python)を探し出す。

# 文字化け対策(UTF-8強制)
try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
except: pass

SNIPER_SCRIPT = "ACCEPT_ALL_MINIMAL.py"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 記憶(Log/Heartbeat)はCドライブの安全地帯に固定（全拠点で共通の書き込み先）
LOG_FILE = r"C:\StockProject\PHOENIX_IMMUNE_LOG.txt"
HEARTBEAT = r"C:\StockProject\sniper_heartbeat.txt"

def find_python_portal():
    """自分を動かしている、あるいは近くにある脳(Python)を探す"""
    # 候補1: 自分を立ち上げた現在実行中のプロセスの実行ファイル
    current_py = sys.executable
    if "pythonw.exe" in current_py.lower() or "python.exe" in current_py.lower():
        return current_py
    
    # 候補2: 自分のフォルダの隣にあるはずの python_embed フォルダ
    # ( dispatcher.vbs が正しく動いていればここにある )
    search_paths = [
        os.path.join(os.path.dirname(BASE_DIR), "python_embed", "pythonw.exe"),
        os.path.join(BASE_DIR, "python_embed", "pythonw.exe"),
    ]
    for p in search_paths:
        if os.path.exists(p):
            return p
            
    return "pythonw.exe" # 最後の手段（PATHに頼る）

PYTHON_EXE = find_python_portal()

def log_event(msg):
    try:
        if not os.path.exists(os.path.dirname(LOG_FILE)):
            os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        with open(LOG_FILE, "a+", encoding="utf-8") as f:
            t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{t}] {msg}\n")
    except: pass

def is_sniper_alive():
    """心音の鮮度で判断"""
    try:
        if os.path.exists(HEARTBEAT):
            with open(HEARTBEAT, "r") as f:
                last_beat = float(f.read().strip())
            if time.time() - last_beat < 120:
                return True
        return False
    except: return False

def revive_sniper():
    try:
        os.chdir(BASE_DIR)
        # 相対パスによる確実な起動
        subprocess.Popen([PYTHON_EXE, SNIPER_SCRIPT], creationflags=subprocess.CREATE_NO_WINDOW)
        log_event(f"SYSTEM: スナイパーを蘇生しました (使用脳: {PYTHON_EXE})")
    except Exception as e:
        log_event(f"ERROR: 蘇生失敗 - {str(e)}")

if __name__ == "__main__":
    log_event(f"SYSTEM: 免疫システム V3.7 起動 (拠点情報: {BASE_DIR})")
    while True:
        if not is_sniper_alive():
            revive_sniper()
        time.sleep(60)
