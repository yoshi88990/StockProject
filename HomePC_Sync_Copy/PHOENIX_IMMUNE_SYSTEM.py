import subprocess
import time
import datetime
import os

# --- PHOENIX IMMUNE SYSTEM (自己免疫・監視プログラム) ---
# 師匠の命により作成された、もう一つの「外部の力」。
# 目的: Phoenix Sniper に万が一未知のバグが発生し、強制終了（死）を迎えた場合、
# それをOS外から検知し、自動で再起動（蘇生）させることで完全な不死を実現する。

SNIPER_SCRIPT_NAME = "ACCEPT_ALL_MINIMAL.py"
STARTUP_VBS = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup", "AUTO_PHOENIX_SNIPER.vbs")
LOG_FILE = r"C:\StockProject\PHOENIX_IMMUNE_LOG.txt"

def log_event(msg):
    """免疫システムの活動記録を密かに残す"""
    try:
        with open(LOG_FILE, "a+", encoding="utf-8") as f:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] {msg}\n")
    except:
        pass

def is_sniper_alive():
    """OSの深部にアクセスし、スナイパーの心音（プロセス）を確認する"""
    try:
        # python.exe と pythonw.exe の両方を検索対象にする（蘇生時は表示用python.exeになるため）
        output = subprocess.check_output(
            'wmic process where "name like \'python%.exe\'" get commandline', 
            shell=True, 
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        if SNIPER_SCRIPT_NAME not in output:
            return False

        # 【フリーズ・ハングアップの検知】(自殺＆蘇生)
        # プロセスがあったとしても、応答なしで固まっているかチェック
        hb_file = r"C:\StockProject\sniper_heartbeat.txt"
        if os.path.exists(hb_file):
            with open(hb_file, "r") as f:
                try:
                    last_beat = float(f.read().strip())
                except:
                    last_beat = time.time()
            
            # スナイパーは30秒周期なので、3分（180秒）以上更新が無ければ「固まっている(脳死)」と判定
            if time.time() - last_beat > 180:
                log_event("CRITICAL: スナイパーが固まっています（心音停止）。フリーズと判定し強制キルします。")
                # 固まったプロセスを強制自殺させる
                subprocess.call(
                    'powershell -Command "Stop-Process -Id (Get-CimInstance Win32_Process -Filter \\"CommandLine LIKE \'%ACCEPT_ALL_MINIMAL.py%\'\\").ProcessId -Force"', 
                    shell=True, 
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                return False
        
        return True
    except Exception:
        pass
    return False

def revive_sniper():
    """蘇生プロトコル: スナイパーの再起動（細胞分裂）"""
    try:
        # 師匠の命令: 蘇生時は通常のVBS（隠れ身）ではなく、最大化ウィンドウで堂々と復活し、
        # 自分が死から蘇ったことを自覚させる引数(--revived)を渡す
        python_exe = r"C:\Users\yoshi\AppData\Local\Python\bin\python.exe"
        script_path = r"c:\StockProject\ACCEPT_ALL_MINIMAL.py"
        cmd = f'powershell -Command "Start-Process -FilePath \'{python_exe}\' -ArgumentList \'{script_path} --revived\' -WindowStyle Maximized"'
        subprocess.call(cmd, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        log_event("CRITICAL: スナイパーの停止またはフリーズを検知。最大化状態での自己蘇生を実行しました。")
    except Exception as e:
        log_event(f"ERROR: 蘇生失敗 - {str(e)}")

if __name__ == "__main__":
    import ctypes
    # プロセス名をリネーム
    try: ctypes.windll.kernel32.SetConsoleTitleW("PHOENIX_IMMUNE_SYSTEM")
    except: pass

    log_event("SYSTEM: =========================================")
    log_event("SYSTEM: 自己免疫プログラム(Watchdog)が監視を開始しました。")
    
    while True:
        # スナイパーが生きているかチェック
        if not is_sniper_alive():
            # もし死んでいれば即座に治癒（再起動）
            revive_sniper()
        
        # 5分間休眠（PCに一切の負荷をかけない極小監視ループ）
        time.sleep(300)
