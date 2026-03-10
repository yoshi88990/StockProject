import os
import time
import datetime
import subprocess
import ctypes

# =========================================================================
# 【PHOENIX SYNCHRONIZER】(自律型DNA・記憶同期プログラム) 
# 目的: 自宅PCが学習した株式知識、備忘録、新たなターゲットリストを
#       24時間常にGitHubと同期(Pull/Push)し、全拠点(会社PC等)で知能を共有する。
# =========================================================================

REPO_DIR = r"C:\Users\yoshi\OneDrive\Weekly report"

def sync_knowledge():
    """Gitを用いて、自律的に学習した知識（コード・備忘録）を完全同期する"""
    try:
        # 1. まず他拠点のDNAを受信 (Pull)
        subprocess.run(["git", "pull", "origin", "master"], cwd=REPO_DIR, capture_output=True, text=True, creationflags=0x08000000)
        
        # 2. このPCの変更点を全て登録
        subprocess.run(["git", "add", "."], cwd=REPO_DIR, capture_output=True, text=True, creationflags=0x08000000)
        
        # 3. 変更をコミット
        commit_msg = f"Auto-Sync Knowledge {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
        res = subprocess.run(["git", "commit", "-m", commit_msg], cwd=REPO_DIR, capture_output=True, text=True, creationflags=0x08000000)
        
        # 4. 変更点がある場合のみ世界へ共有 (Push)
        if "nothing to commit" not in res.stdout:
            subprocess.run(["git", "push", "origin", "HEAD"], cwd=REPO_DIR, capture_output=True, text=True, creationflags=0x08000000)
    except Exception as e:
        pass

if __name__ == "__main__":
    try: ctypes.windll.kernel32.SetConsoleTitleW("PHOENIX_SYNCHRONIZER")
    except: pass

    # 初回起動時に同期
    sync_knowledge()

    # 24時間・無音待機ループ
    while True:
        # 30分に1回、自動的に記憶を強制同期させる（サステナビリティ）
        time.sleep(1800)
        sync_knowledge()
