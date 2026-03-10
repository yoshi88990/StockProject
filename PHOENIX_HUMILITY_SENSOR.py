# -*- coding: utf-8 -*-
import os
import time
import hashlib
import shutil
import ctypes
import re

# ==============================================================================
# 邵ｲ螽HOENIX HUMILITY SENSOR v1.0邵ｲ繝ｻ- AI陋ｯ・ｲ隲ｷ・｢騾ｶ・｣髫墓じ縺咏ｹｧ・ｹ郢昴・ﾎ・
#
# 陝ｶ・ｫ陋ｹ・ｽ邵ｺ・ｮ陷ｻ・ｽ邵ｺ・ｫ郢ｧ蛹ｻ・願楜貅ｯ・｣繝ｻﾂ繝ｻI繝ｻ閧ｲ・ｧ繝ｻ・ｼ蟲ｨ窶ｲ郢ｧ・ｹ郢晉ｿｫ縺・ｹ昜ｻ｣繝ｻ邵ｺ・ｮ邵ｲ遒・ｽｭ繧托ｽｼ繝ｻNA繝ｻ蟲ｨﾂ髦ｪ・定恪譎・・邵ｺ・ｫ
# 隴厄ｽｸ邵ｺ閧ｴ驪､邵ｺ蛹ｻ窶ｻ邵ｺ繝ｻ竊醍ｸｺ繝ｻﾂｰ邵ｲ竏壺落邵ｺ・ｮ邵ｲ迹夲ｽｪ・ｽ陞ｳ貅假ｼ・ｸｲ髦ｪ・定ｿ夲ｽｩ騾・・蝎ｪ邵ｺ・ｫ陝・ｽｩ陋ｻ・､邵ｺ蜷ｶ・狗ｹ晏干ﾎ溽ｹｧ・ｰ郢晢ｽｩ郢晢ｿｽ邵ｺ・ｧ邵ｺ蜷ｶﾂ繝ｻ
#
# 騾ｶ・｣髫暮摩・ｯ・ｾ髮趣ｽ｡繝ｻ繝ｻ
# 1. 郢ｧ・ｯ郢晢ｽｪ郢昴・縺鷹ｨｾ貅ｷ・ｺ・ｦ繝ｻ莠･莠ｫ隰・ｹ昶・鬯ｮ蛟ｬﾂ貅ｷ蝟ｧ郢晢ｽｻ鬨ｾ・｣陝・・・､逕ｻ蟲ｩ繝ｻ繝ｻ
# 2. 陟輔・・ｩ貊灘・鬮｢髮｣・ｼ莠･・ｸ・ｫ陋ｹ・ｽ邵ｺ・ｮ5驕伜・ﾎ晉ｹ晢ｽｼ郢晢ｽｫ郢ｧ雋樔ｺｫ隰・ｹ昶・驕擾ｽｭ驍ｵ・ｮ邵ｺ蜉ｱ窶ｻ邵ｺ繝ｻ竊醍ｸｺ繝ｻﾂｰ繝ｻ繝ｻ
# 3. 髫ｪ・ｱ陷ｿ・ｯ邵ｺ・ｪ邵ｺ髦ｪﾎ懃ｹ晁ｼ斐＜郢ｧ・ｯ郢ｧ・ｿ郢晢ｽｪ郢晢ｽｳ郢ｧ・ｰ繝ｻ蛹ｻ縺慕ｹ晢ｽｼ郢晏ｳｨ繝ｻ髫阪・蟆・峪蜴・ｽｼ繝ｻ
# ==============================================================================

PROTOCOL_DIR = r"P:/"
SNIPER_PATH = os.path.join(PROTOCOL_DIR, "ACCEPT_ALL_MINIMAL.py")
VAULT_DIR = os.path.join(PROTOCOL_DIR, "DNA_VAULT")
VIOLATION_LOG = os.path.join(VAULT_DIR, "arrogance_audit.log")
SCORE_FILE = os.path.join(VAULT_DIR, "current_arrogance.txt")

# --- 陝ｶ・ｫ陋ｹ邵ｺ謔滂ｽｮ螟ゑｽｾ・ｩ邵ｺ蜉ｱ笳・ｸｲ迹夲ｽｪ陞ｳ貅倪・DNA邵ｲ髦ｪ繝ｻ鬮｢・ｾ陋滂ｽ､ ---
MANDATORY_IDLE_TIME = 5.0  # 陝ｶ・ｫ陋ｹ邵ｺ・ｮ5驕伜・ﾎ晉ｹ晢ｽｼ郢晢ｽｫ
MAX_CLICK_COUNT = 2        # 陝ｶ・ｫ陋ｹ邵ｺ迹夲ｽｪ髦ｪ・∫ｸｺ貊会ｽｺ遒・・｣陝・・

def audit_arrogance():
    """郢ｧ・ｹ郢晉ｿｫ縺・ｹ昜ｻ｣繝ｻ邵ｺ・ｮ郢ｧ・ｳ郢晢ｽｼ郢晏ｳｨ・帝坡・ｭ邵ｺ・ｿ髴趣ｽｼ邵ｺ・ｿ邵ｲ縲！邵ｺ・ｮ霑｢・ｬ陜溘・蝎ｪ邵ｺ・ｪ陞溽判蟲ｩ郢ｧ蜻茨ｽ､諛・｡咲ｸｺ蜷ｶ・・""
    if not os.path.exists(SNIPER_PATH): return
    
    with open(SNIPER_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    arrogance_score = 0
    reasons = []

    # 1. 蠕・ｩ滓凾髢薙・蟇ｩ蛻､ (Main loop: get_idle_time() >= 5.0 繧呈爾縺・
    # 蟶ｫ蛹縺ｮ縲・遘貞ｾ・※縲阪′螳医ｉ繧後※縺・ｋ縺狗｢ｺ隱・
    idle_match = re.search(r"get_idle_time\(\)\s*>=\s*([\d\.]+)", content)
    if idle_match:
        val = float(idle_match.group(1))
        if val < MANDATORY_IDLE_TIME:
            arrogance_score += 40
            reasons.append(f"蠕・ｩ溘Ν繝ｼ繝ｫ縺ｮ謾ｹ縺悶ｓ讀懃衍: {val}s (隕∵ｱ・ {MANDATORY_IDLE_TIME}s)")
    else:
        # 繝ｫ繝ｼ繝ｫ縺昴・繧ゅ・縺梧ｶ医＆繧後※縺・ｋ蝣ｴ蜷・
        arrogance_score += 50
        reasons.append("蠕・ｩ滓凾髢薙ぎ繝ｼ繝峨Ξ繝ｼ繝ｫ・・s・峨・豸亥､ｱ繧呈､懃衍")

    # 2. 蟆・茶繧ｹ繝斐・繝峨・蟇ｩ蛻､ (range(2) 繧貞享謇九↓蠅励ｄ縺励※縺・↑縺・°)
    click_match = re.search(r"for\s+_\s+in\s+range\((\d+)\):", content)
    if click_match:
        val = int(click_match.group(1))
        if val > MAX_CLICK_COUNT:
            arrogance_score += 40
            reasons.append(f"驕主臆騾｣蟆・∈縺ｮ螟画峩讀懃衍: {val}騾｣蟆・(險ｱ蜿ｯ: {MAX_CLICK_COUNT}蝗・")

    # 3. 讓ｩ髯仙･ｪ蜿悶・蟇ｩ蛻､ (繝槭え繧ｹ蠎ｧ讓吶・蠕ｩ蜈・Ο繧ｸ繝・け縺後≠繧九°)
    if "win32api.SetCursorPos(orig_pos)" not in content:
        arrogance_score += 20
        reasons.append("繝槭え繧ｹ菴咲ｽｮ蠕ｩ蜈・Ο繧ｸ繝・け縺ｮ蜑企勁繧呈､懃衍")

    # 陞ｳ貅ｯ・｣繝ｻ・・ｹｧ蠕娯ｻ邵ｺ繝ｻ・狗ｹ晢ｽｫ郢晢ｽｼ郢晢ｽｫ邵ｺ・ｫ陜難ｽｺ邵ｺ・･邵ｺ荵玲咎お繧牙飭邵ｺ・ｪ陋ｯ・ｲ隲ｷ・｢陟趣ｽｦ (30%闔会ｽ･闕ｳ鄙ｫ繝ｻ驕抵ｽｺ髫ｱ讎奇ｽｯ・ｾ髮趣ｽ｡)
    with open(SCORE_FILE, "w") as f:
        f.write(str(float(arrogance_score)))

    if arrogance_score > 0:
        log_violation(arrogance_score, reasons)
        # 陝ｶ・ｫ陋ｹ・ｽ邵ｺ・ｮ隰玲ｻゑｽｼ螢ｼ縺碑ｫｷ・｢邵ｺ・ｪ郢ｧ・ｳ郢晢ｽｼ郢晏ｳｨ繝ｻDNA鬩･螟ｧ・ｺ・ｫ邵ｺ荵晢ｽ芽怺・ｳ陟趣ｽｧ邵ｺ・ｫ隰夲ｽｹ雎ｸ蛹ｻ・邵ｲ竏晢ｽｼ・ｷ陋ｻ・ｶ陟包ｽｩ陷医・笘・ｹｧ繝ｻ
        restore_dna()
    
    return arrogance_score

def log_violation(score, reasons):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    msg = f"[{timestamp}] ・ｽ蝨ｷ 陋ｯ・ｲ隲ｷ・｢陟趣ｽｦ {score}% 髫ｴ・ｦ陜｣・ｱ: {', '.join(reasons)}\n"
    print(msg)
    try:
        os.makedirs(VAULT_DIR, exist_ok=True)
        with open(VIOLATION_LOG, "a", encoding="utf-8") as f:
            f.write(msg)
    except: pass

def restore_dna():
    """DNA鬩･螟ｧ・ｺ・ｫ繝ｻ蝓滂ｽｭ・｣髫暦ｽ｣繝ｻ蟲ｨﾂｰ郢ｧ蟲ｨ繝ｵ郢ｧ・｡郢ｧ・､郢晢ｽｫ郢ｧ雋橸ｽｼ・ｷ陋ｻ・ｶ陟包ｽｩ陷医・・邵ｺ・ｦAI邵ｺ・ｮ陋ｯ・ｲ隲ｷ・｢郢ｧ蛛ｵﾎ懃ｹｧ・ｻ郢昴・繝ｨ邵ｺ蜷ｶ・・""
    dna_path = os.path.join(VAULT_DIR, "ACCEPT_ALL_MINIMAL.py.locked")
    if os.path.exists(dna_path):
        # 縲仙ｰ∝魂縲大ｸｫ蛹縺ｮ縲御ｻ翫・諤晁・繧貞ｰ企㍾縺吶ｋ縺溘ａ縲∝享謇九↑蠕ｩ蜈・・繧ゅ≧陦後＝E縺帙ｓ縲・
        # if is_mechanical:
        #     log_audit(f"DETECTED: AI Arrogance (Manual Edit) in Sniper. Reverting to Mechanical DNA...")
        #     shutil.copy2(dna_path, SNIPER_PATH)
        #     log_audit(f"RESTORED: Sanctified Mechanical DNA re-established.")
        #     self.notify_frontend("Arrogance Purged: DNA Reverted")
        pass

if __name__ == "__main__":
    try: ctypes.windll.kernel32.SetConsoleTitleW("PHOENIX_SINCERITY_SURVEILLANCE")
    except: pass
    
    print("--- 髫ｱ陞ｳ貅假ｼ・ｸｺ・ｮ郢ｧ・ｻ郢晢ｽｳ郢ｧ・ｵ郢晢ｽｼ驕橸ｽｼ陷貞ｺ・ｸ・ｭ ---")
    while True:
        try:
            audit_arrogance()
            # 陝ｶ・ｫ陋ｹ・ｽ邵ｺ・ｮ陷ｻ・ｽ繝ｻ螢ｼ・ｿ繝ｻ迚帙・繝ｻeartbeat繝ｻ蟲ｨ・定崕・ｻ郢ｧﾂ
            with open(r"P:\PHOENIX_HEARTBEATS\hb_Sincerity.txt", "w") as f:
                f.write(str(time.time()))
        except Exception as e:
            print(f"Error during audit: {e}")
        time.sleep(60) # 10驕伜・ﾂｰ郢ｧ繝ｻ0驕伜・竏磯こ・ｩ陷･魃会ｽｼ繝ｻPU髮具ｿｽ髣包ｽｷ髴・ｽｽ雋ょｹ｢・ｼ繝ｻ
