import subprocess
import time
import datetime
import os
import sys

# =========================================================================
# 【PHOENIX IMMUNE SYSTEM v4.0】(統一ドライブ P: 対応版)
# 目的: スナイパーの生存確認と蘇生。ただし「明示的な停止」は尊重する。
# =========================================================================

# 文字化け対策(UTF-8強制)
try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
except: pass

# 統一ドライブ規格
PROTOCOL_DIR = r"P:/"
SNIPER_SCRIPT = "ACCEPT_ALL_MINIMAL.py"
PYTHON_EXE = r"C:\Users\kanku\OneDrive\Weekly report\python_embed\pythonw.exe"

# ログと心音の場所（Pドライブに集約）
LOG_FILE = os.path.join(PROTOCOL_DIR, "PHOENIX_IMMUNE_LOG.txt")
HEARTBEAT = os.path.join(PROTOCOL_DIR, "PHOENIX_HEARTBEATS", "hb_Mechanical.txt")
STOP_SIGNAL = os.path.join(PROTOCOL_DIR, "STOP_PHOENIX") # このファイルがあれば停止

def log_event(msg):
    try:
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
            # 2分（120秒）以内に更新されていれば生存とみなす
            if time.time() - last_beat < 120:
                return True
        return False
    except: return False

def revive_sniper():
    if os.path.exists(STOP_SIGNAL):
        # 停止信号がある場合は蘇生しない
        return

    try:
        script_path = os.path.join(PROTOCOL_DIR, SNIPER_SCRIPT)
        if os.path.exists(script_path):
            # CREATE_NO_WINDOW (0x08000000) でバックグラウンド起動
            subprocess.Popen([PYTHON_EXE, script_path], 
                             cwd=PROTOCOL_DIR,
                             creationflags=0x08000000)
            log_event(f"SYSTEM: スナイパーを蘇生しました。")
        else:
            log_event(f"ERROR: スクリプトが見つかりません: {script_path}")
    except Exception as e:
        log_event(f"ERROR: 蘇生失敗 - {str(e)}")

if __name__ == "__main__":
    log_event(f"SYSTEM: 免疫システム v4.0 起動 (稼働開始)")
    
    # 起動時に一度だけ停止信号を掃除（必要なら）
    # if os.path.exists(STOP_SIGNAL): os.remove(STOP_SIGNAL)

    while True:
        # 停止信号が「ない」時だけ監視を行う
        if not os.path.exists(STOP_SIGNAL):
            if not is_sniper_alive():
                log_event("WARNING: スナイパーの沈黙を検知しました。蘇生を試みます。")
                revive_sniper()
        else:
            # 停止信号がある間は、ログに一度だけ記録して静観する
            pass

        time.sleep(30) # 30秒間隔で精密にチェック
