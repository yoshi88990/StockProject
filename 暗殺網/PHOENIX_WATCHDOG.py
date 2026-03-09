import subprocess
import time
import os

# ==============================================================================
# 【PHOENIX SMART WATCHDOG】 (自己免疫システムの浄化版)
# 
# 旧式の「ターミナルを最大化して暴れる」蘇生システムを完全に廃止。
# 新しい「空っぽの器 (PHOENIX_SMART_SNIPER.py)」が静かに生きているか監視し、
# 死んでいればバックグラウンドで（完全無音・無画面で）再起動する。
# ==============================================================================

SNIPER_SCRIPT_NAME = "PHOENIX_SMART_SNIPER.py"

def is_sniper_alive():
    try:
        output = subprocess.check_output(
            'wmic process where "name like \'python%.exe\'" get commandline', 
            shell=True, 
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        if SNIPER_SCRIPT_NAME not in output:
            return False

        # OneDriveを汚染しないように "%TEMP%" に移した心音を確認する
        hb_file = os.path.join(os.getenv("TEMP"), "phoenix_sniper_heartbeat.txt")
        if os.path.exists(hb_file):
            with open(hb_file, "r") as f:
                try:
                    last_beat = float(f.read().strip())
                except:
                    last_beat = time.time()
            
            # スナイパーは30秒呼吸。3分(180秒)更新がなければハングアップとみなす
            if time.time() - last_beat > 180:
                subprocess.call(
                    f'wmic process where "commandline like \'%{SNIPER_SCRIPT_NAME}%\'" call terminate', 
                    shell=True, 
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                return False
        return True
    except:
        return False

def revive_sniper():
    """【Smart Revive】ターミナルを出さず、完全背面で蘇生する"""
    try:
        python_exe = r"C:\Users\yoshi\AppData\Local\Python\bin\pythonw.exe"
        script_path = r"c:\Users\yoshi\OneDrive\Weekly report\Phoenix_Protocol\暗殺網\PHOENIX_SMART_SNIPER.py"
        # 以前の『-WindowStyle Maximized』という暴挙を捨て、完全に隠蔽(pythonw)して起動
        cmd = f'"{python_exe}" "{script_path}"'
        subprocess.Popen(cmd, shell=False, creationflags=subprocess.CREATE_NO_WINDOW)
    except:
        pass

if __name__ == "__main__":
    while True:
        if not is_sniper_alive():
            revive_sniper()
        time.sleep(300)
