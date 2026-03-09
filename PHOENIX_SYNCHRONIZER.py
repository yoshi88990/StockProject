import os
import time
import datetime
import subprocess
import ctypes

# =========================================================================
# 【PHOENIX SYNCHRONIZER】(自律型DNA・記憶同期プログラム) 
# ぼくが目的: アシスタントが進化・学習したコードや備忘録を
#       24時間常にGitHubと同期(Pull/Push)し、全拠点(会社PC⇔自宅PC)で知能を共有(シナプス化)する。
# =========================================================================

REPO_DIR = r"C:\StockProject"

def sync_knowledge():
    """Gitを用いて、自律的に学習した知識（コード・備忘録）を完全同期する"""
    try:
        # 1. 首先他拠点で進化したDNAを受信（Pull）
        subprocess.run(["powershell", "-Command", "git pull origin master"], cwd=REPO_DIR, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        
        # 2. 自分（このPC）が学習・変更した内容があれば全て登録
        subprocess.run(["powershell", "-Command", "git add ."], cwd=REPO_DIR, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        
        # 3. 変更をコミット（無音）
        commit_msg = f"Auto-Sync Phoenix Protocol {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
        res = subprocess.run(["powershell", "-Command", f'git commit -m "{commit_msg}"'], cwd=REPO_DIR, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        
        # 4. 新しい記憶があれば共有（Push）
        if "nothing to commit" not in res.stdout:
            subprocess.run(["powershell", "-Command", "git push origin HEAD"], cwd=REPO_DIR, capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
    except Exception as e:
        pass

if __name__ == "__main__":
    try: ctypes.windll.kernel32.SetConsoleTitleW("PHOENIX_SYNCHRONIZER")
    except: pass

    # PC起動時に初回の同期を行う
    sync_knowledge()

    # 以降、24時間・30分周期（1800秒）で自動同期
    while True:
        time.sleep(1800)
        sync_knowledge()
