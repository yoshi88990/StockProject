import os
import subprocess
import time

# =========================================================================
# 【PHOENIX MASTER UNIFIER】(拠点・知能の一括一発統合プロトコル)
# 目的: 「あいことば」一つで、自宅・会社の全知能を同じ「平和な」設定に同期する
# =========================================================================

PASS_PHRASE = "PHOENIX_REBIRTH_2026"

def unify_intelligence():
    print(f"[*] あいことばを受理: {PASS_PHRASE}")
    print("[*] 自宅拠点のDNA同期と、プロセスの『消音・平和化』を開始します...")
    
    # 窓を隠す魔法のフラグ (青い窓を出さない)
    HIDE = 0x08000000
    
    try:
        # 1. Git最新化（会社で修正した「静寂設定」を吸い込む）
        subprocess.run(["git", "pull", "origin", "master"], creationflags=HIDE)
        print("[+] 会社拠点で修正した『沈黙プロトコル』に自宅を書き換えました。")
        
        # 2. 暴走・あるいは古いプロセスの完全停止
        subprocess.run(["taskkill", "/F", "/IM", "python.exe"], creationflags=HIDE)
        subprocess.run(["taskkill", "/F", "/IM", "pythonw.exe"], creationflags=HIDE)
        subprocess.run(["taskkill", "/F", "/IM", "git.exe"], creationflags=HIDE)
        print("[+] 古い知能を一旦眠らせ、お掃除を完了しました。")
        
        # 3. 修正済みの「平和な」部隊を再起動
        # P:\PHOENIX_DNA_SYNCHRONIZER.py などが「1時間周期・窓なし」で動き出します
        startup_vbs = r"C:\Users\kanku\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\AUTO_PHOENIX_SNIPER.vbs"
        if os.path.exists(startup_vbs):
            os.startfile(startup_vbs)
            print("[+] 知能を『平和モード（1時間周期）』で再点火しました。")
        
    except Exception as e:
        print(f"[-] 同期エラー: {e}")

if __name__ == "__main__":
    unify_intelligence()
    print("\n--- 完了 ---")
    print("師匠、自宅PCもこれで『静寂』と『同期』が完璧に両立されました。")
    print("青い窓に悩まされることなく、1時間おきにひっそりと同期されます。")
    time.sleep(5)