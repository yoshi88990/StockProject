# -*- coding: utf-8 -*-
import os
import subprocess
import time
from datetime import datetime

# ==============================================================================
# 縲娠HOENIX DNA SYNCHRONIZER縲・v1.2 [ABSOLUTE SILENCE]
#
# 繝ｻGit謫堺ｽ懈凾縺ｮ繧ｳ繝ｳ繧ｽ繝ｼ繝ｫ繧ｦ繧｣繝ｳ繝峨え・医メ繧ｫ繝√き・峨ｒOS繝ｬ繝吶Ν縺ｧ蟆∵ｮｺ縺励∪縺励◆縲・
# ==============================================================================

PROJECT_DIR = r"P:/"

def run_git_sync():
    try:
        os.chdir(PROJECT_DIR)
        
        # 縲宣㍾隕√舛REATE_NO_WINDOW (0x08000000) 繧呈欠螳壹＠縺ｦ繧ｳ繝ｳ繝代う繝ｫ
        # 縺薙ｌ縺ｫ繧医ｊ縲√＞縺九↑繧句ｴ蜷医ｂ譁ｰ縺励＞繧ｳ繝ｳ繧ｽ繝ｼ繝ｫ遯薙′菴懈・縺輔ｌ縺ｾ縺帙ｓ縲・
        CREATE_NO_WINDOW = 0x08000000

        # 0. 蜷ｸ蠑・(Pull)
        subprocess.run(["git", "pull", "origin", "master"], creationflags=0x08000000)

        # 1. 螟画峩縺後≠繧九°遒ｺ隱・
        status = subprocess.check_output(
            ["git", "status", "--porcelain"], 
            creationflags=0x08000000
        ).decode('utf-8')
        
        # 2. 譛ｪPush縺ｮ繧ｳ繝溘ャ繝医′縺ゅｋ縺狗｢ｺ隱・
        unpushed = subprocess.check_output(
            ["git", "cherry", "-v"], 
            creationflags=0x08000000
        ).decode('utf-8')

        if status or unpushed:
            # 3. 蜈ｨ縺ｦ繧偵せ繝・・繧ｸ
            subprocess.run(["git", "add", "."], check=True, creationflags=0x08000000)
            
            # 4. 螟画峩縺後≠繧句ｴ蜷医・縺ｿ繧ｳ繝溘ャ繝・
            if status:
                msg = f"Auto-Sync DNA: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                subprocess.run(["git", "commit", "-m", msg], check=True, creationflags=0x08000000)
            
            # 5. 謚墓憧 (Push)
            subprocess.run(["git", "push", "origin", "master"], check=True, creationflags=0x08000000)
            
    except Exception:
        pass

if __name__ == "__main__":
    while True:
        try:
            # 蟶ｫ蛹縺ｮ蜻ｽ縺ｮ鮠灘虚(Heartbeat)繧貞綾繧
            hb_dir = r"P:\PHOENIX_HEARTBEATS"
            if not os.path.exists(hb_dir): os.makedirs(hb_dir)
            with open(os.path.join(hb_dir, "hb_Receptor.txt"), "w") as f:
                f.write(str(time.time()))
        except: pass
        run_git_sync()
        # 蟶ｫ蛹縺ｸ縺ｮ螳峨ｉ縺趣ｼ・譎る俣・・600遘抵ｼ峨↓荳蠎ｦ縺ｮ蜷梧悄縺ｧPC繧貞ｮ悟・縺ｫ莨代∪縺帙ｋ
        time.sleep(3600)
