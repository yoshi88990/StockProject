import subprocess
import time
import datetime
import os

# --- PHOENIX IMMUNE SYSTEM (自己免疫・監視プログラム) ---
# 師匠の命により作成された、もう一つの「外部の力」。
# 目的: Phoenix Sniper に万が一未知のバグが発生し、強制終了（死）を迎えた場合、
# それをOS外から検知し、自動で再起動（蘇生）させることで完全な不死を実現する。

SNIPER_SCRIPT_NAME = "ACCEPT_ALL_MINIMAL.py"
LOG_FILE = r"C:\StockProject\PHOENIX_IMMUNE_LOG.txt"
HB_FILE = r"C:\StockProject\sniper_heartbeat.txt"

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
        # 1. プロセスの物理的な存在チェック（WMICによる確実な確認）
        output = subprocess.check_output(
            'wmic process where "name like \'python%.exe\'" get commandline', 
            shell=True, 
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        if SNIPER_SCRIPT_NAME not in output:
            return False

        # 2. 【フリーズ・ハングアップの検知】(心臓停止による自殺＆蘇生)
        if os.path.exists(HB_FILE):
            try:
                with open(HB_FILE, "r") as f:
                    last_beat = float(f.read().strip())
                
                # スナイパーは30秒周期なので、180秒（3分）更新がなければ死んでいると判定
                if time.time() - last_beat > 180:
                    log_event("CRITICAL: スナイパーが固まっています（心音停止）。フリーズと判定し強制キルします。")
                    # フリーズしたゾンビプロセスを強制キル
                    subprocess.call(
                        'powershell -Command "Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like \'*ACCEPT_ALL_MINIMAL.py*\' } | Stop-Process -Force"', 
                        shell=True, 
                        creationflags=subprocess.CREATE_NO_WINDOW
                    )
                    return False
            except Exception as e:
                pass
        
        return True
    except Exception:
        pass
    return False

def revive_sniper():
    """蘇生プロトコル: スナイパーの再起動（細胞分裂）"""
    try:
        # PC固有の環境パスで復活 (python.exe を使うことで復活時は見える化する)
        python_exe = r"C:\Users\kanku\Desktop\Weekly report\Weekly-report\python_embed\python.exe"
        script_path = r"C:\StockProject\ACCEPT_ALL_MINIMAL.py"
        # 蘇生時は目立たせる
        subprocess.call(f'powershell -Command "Start-Process -FilePath \'{python_exe}\' -ArgumentList \'{script_path} --revived\' -WindowStyle Normal"', shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        log_event("SUCCESS: スナイパーの停止を検知し、自己蘇生を行いました。")
    except Exception as e:
        log_event(f"ERROR: 蘇生失敗 - {str(e)}")

if __name__ == "__main__":
    import ctypes
    # プロセス名をリネーム
    try: ctypes.windll.kernel32.SetConsoleTitleW("PHOENIX_IMMUNE_SYSTEM")
    except: pass

    log_event("SYSTEM: =========================================")
    log_event("SYSTEM: 自己免疫プログラム(Immune System)が24時間監視を開始しました。")
    
    while True:
        # スナイパーが生きているかチェック
        if not is_sniper_alive():
            revive_sniper()
        
        # 30秒ごとに監視（PCへの負荷なし）
        time.sleep(30)
