import os
import subprocess
import time
from datetime import datetime

# ==============================================================================
# 【PHOENIX DNA SYNCHRONIZER】 v1.2 [ABSOLUTE SILENCE]
#
# ・Git操作時のコンソールウィンドウ（チカチカ）をOSレベルで封殺しました。
# ==============================================================================

PROJECT_DIR = r"P:/"

def run_git_sync():
    try:
        os.chdir(PROJECT_DIR)
        
        # 【重要】CREATE_NO_WINDOW (0x08000000) を指定してコンパイル
        # これにより、いかなる場合も新しいコンソール窓が作成されません。
        CREATE_NO_WINDOW = 0x08000000

        # 0. 吸引 (Pull)
        subprocess.run(["git", "pull", "origin", "master"], creationflags=CREATE_NO_WINDOW)

        # 1. 変更があるか確認
        status = subprocess.check_output(
            ["git", "status", "--porcelain"], 
            creationflags=CREATE_NO_WINDOW
        ).decode('utf-8')
        
        # 2. 未Pushのコミットがあるか確認
        unpushed = subprocess.check_output(
            ["git", "cherry", "-v"], 
            creationflags=CREATE_NO_WINDOW
        ).decode('utf-8')

        if status or unpushed:
            # 3. 全てをステージ
            subprocess.run(["git", "add", "."], check=True, creationflags=CREATE_NO_WINDOW)
            
            # 4. 変更がある場合のみコミット
            if status:
                msg = f"Auto-Sync DNA: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                subprocess.run(["git", "commit", "-m", msg], check=True, creationflags=CREATE_NO_WINDOW)
            
            # 5. 投擲 (Push)
            subprocess.run(["git", "push", "origin", "master"], check=True, creationflags=CREATE_NO_WINDOW)
            
    except Exception:
        pass

if __name__ == "__main__":
    while True:
        try:
            # 師匠の命：心拍(Heartbeat)を刻む
            with open(r"P:\PHOENIX_HEARTBEATS\hb_Receptor.txt", "w") as f:
                f.write(str(time.time()))
        except: pass
        run_git_sync()
        time.sleep(120) # 10秒から2分へ緩和（Git操作の負荷軽減）
