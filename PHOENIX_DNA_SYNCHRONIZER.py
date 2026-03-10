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
        subprocess.run(["git", "pull", "origin", "master"], creationflags=0x08000000)

        # 1. 変更があるか確認
        status = subprocess.check_output(
            ["git", "status", "--porcelain"], 
            creationflags=0x08000000
        ).decode('utf-8')
        
        # 2. 未Pushのコミットがあるか確認
        unpushed = subprocess.check_output(
            ["git", "cherry", "-v"], 
            creationflags=0x08000000
        ).decode('utf-8')

        if status or unpushed:
            # 3. 全てをステージ
            subprocess.run(["git", "add", "."], check=True, creationflags=0x08000000)
            
            # 4. 変更がある場合のみコミット
            if status:
                msg = f"Auto-Sync DNA: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                subprocess.run(["git", "commit", "-m", msg], check=True, creationflags=0x08000000)
            
            # 5. 投擲 (Push)
            subprocess.run(["git", "push", "origin", "master"], check=True, creationflags=0x08000000)
            
    except Exception:
        pass

if __name__ == "__main__":
    while True:
        try:
            # 師匠の命の鼓動(Heartbeat)を刻む
            hb_dir = r"P:\PHOENIX_HEARTBEATS"
            if not os.path.exists(hb_dir): os.makedirs(hb_dir)
            with open(os.path.join(hb_dir, "hb_Receptor.txt"), "w") as f:
                f.write(str(time.time()))
        except: pass
        run_git_sync()
        # 師匠への安らぎ：1時間（3600秒）に一度の同期でPCを完全に休ませる
        time.sleep(3600)
