# -*- coding: utf-8 -*-
import os
import subprocess
import time
import shutil

# =========================================================================
# 【PHOENIX MASTER UNIFIER】(拠点・知能の一括一発統合プロトコル)
# =========================================================================

PASS_PHRASE = "/resume"

def unify_intelligence():
    print("[*] Starting Unification Protocol...")
    
    HIDE = 0x08000000
    
    try:
        # 1. Git Pull
        print("[*] Pulling latest DNA from GitHub...")
        subprocess.run(["git", "pull", "origin", "master"], creationflags=HIDE)
        
        # 2. Purge Old Vaults (The Ghost Nest)
        print("[*] Purging legacy vaults and ghost nests...")
        purge_targets = [
            r"P:\DNA_VAULT",
            r"P:\DNA_SEED_STASH",
            r"P:\STABILIZER_V36_BACKUP",
            r"P:\ENCRYPTED_VAULT_EXHAUST",
            r"P:\INTELLIGENCE_STASH",
            r"P:\OFFSHORE_VAULT",
            r"P:\CLOUD_VANGUARD\DATA_VAULT", r"P:\HomePC_Sync_Copy", r"P:\p_U"
        ]
        for target in purge_targets:
            if os.path.exists(target):
                try:
                    shutil.rmtree(target)
                    print(f"[+] Purged: {target}")
                except: pass

        # 3. Kill running processes
        print("[*] Terminating legacy processes...")
        subprocess.run(["taskkill", "/F", "/IM", "python.exe"], creationflags=HIDE)
        subprocess.run(["taskkill", "/F", "/IM", "pythonw.exe"], creationflags=HIDE)
        subprocess.run(["taskkill", "/F", "/IM", "git.exe"], creationflags=HIDE)
        
        # 4. Restart Peace Mode
        startup_vbs = r"P:\PHOENIX_LAUNCH_WEB.vbs"
        if os.path.exists(startup_vbs):
            os.startfile(startup_vbs)
            print("[+] Dashboard and Core restarted in Peace Mode.")
        
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    # User just provides the phrase, we handle the rest
    unify_intelligence()
    print("\n--- COMPLETE ---")
    time.sleep(2)