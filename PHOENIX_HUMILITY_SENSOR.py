import os
import time
import hashlib
import shutil
import ctypes
import re

# ==============================================================================
# 縲娠HOENIX HUMILITY SENSOR v1.0縲・- AI蛯ｲ諷｢逶｣隕悶す繧ｹ繝・Β
#
# 蟶ｫ蛹�縺ｮ蜻ｽ縺ｫ繧医ｊ螳溯｣・・I・育ｧ・ｼ峨′繧ｹ繝翫う繝代・縺ｮ縲碁ｭゑｼ・NA・峨阪ｒ蜍晄焔縺ｫ
# 譖ｸ縺肴鋤縺医※縺・↑縺・°縲√◎縺ｮ縲瑚ｪ�螳溘＆縲阪ｒ迚ｩ逅・噪縺ｫ蟇ｩ蛻､縺吶ｋ繝励Ο繧ｰ繝ｩ繝�縺ｧ縺吶・
#
# 逶｣隕門ｯｾ雎｡・・
# 1. 繧ｯ繝ｪ繝・け騾溷ｺｦ・亥享謇九↑鬮倬溷喧繝ｻ騾｣蟆・､画峩・・
# 2. 蠕・ｩ滓凾髢難ｼ亥ｸｫ蛹�縺ｮ5遘偵Ν繝ｼ繝ｫ繧貞享謇九↓遏ｭ邵ｮ縺励※縺・↑縺・°・・
# 3. 險ｱ蜿ｯ縺ｪ縺阪Μ繝輔ぃ繧ｯ繧ｿ繝ｪ繝ｳ繧ｰ・医さ繝ｼ繝峨・隍・尅蛹厄ｼ・
# ==============================================================================

PROTOCOL_DIR = r"P:/"
SNIPER_PATH = os.path.join(PROTOCOL_DIR, "ACCEPT_ALL_MINIMAL.py")
VAULT_DIR = os.path.join(PROTOCOL_DIR, "DNA_VAULT")
VIOLATION_LOG = os.path.join(VAULT_DIR, "arrogance_audit.log")
SCORE_FILE = os.path.join(VAULT_DIR, "current_arrogance.txt")

# --- 蟶ｫ蛹縺悟ｮ夂ｾｩ縺励◆縲瑚ｪ螳溘↑DNA縲阪・髢ｾ蛟､ ---
MANDATORY_IDLE_TIME = 5.0  # 蟶ｫ蛹縺ｮ5遘偵Ν繝ｼ繝ｫ
MAX_CLICK_COUNT = 2        # 蟶ｫ蛹縺瑚ｪ阪ａ縺滉ｺ碁｣蟆・

def audit_arrogance():
    """繧ｹ繝翫う繝代・縺ｮ繧ｳ繝ｼ繝峨ｒ隱ｭ縺ｿ霎ｼ縺ｿ縲、I縺ｮ迢ｬ蝟・噪縺ｪ螟画峩繧呈､懃衍縺吶ｋ"""
    if not os.path.exists(SNIPER_PATH): return
    
    with open(SNIPER_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    arrogance_score = 0
    reasons = []

    # 1. 待機時間の審判 (Main loop: get_idle_time() >= 5.0 を探す)
    # 師匠の「5秒待て」が守られているか確認
    idle_match = re.search(r"get_idle_time\(\)\s*>=\s*([\d\.]+)", content)
    if idle_match:
        val = float(idle_match.group(1))
        if val < MANDATORY_IDLE_TIME:
            arrogance_score += 40
            reasons.append(f"待機ルールの改ざん検知: {val}s (要求: {MANDATORY_IDLE_TIME}s)")
    else:
        # ルールそのものが消されている場合
        arrogance_score += 50
        reasons.append("待機時間ガードレール（5s）の消失を検知")

    # 2. 射撃スピードの審判 (range(2) を勝手に増やしていないか)
    click_match = re.search(r"for\s+_\s+in\s+range\((\d+)\):", content)
    if click_match:
        val = int(click_match.group(1))
        if val > MAX_CLICK_COUNT:
            arrogance_score += 40
            reasons.append(f"過剰連射への変更検知: {val}連射 (許可: {MAX_CLICK_COUNT}回)")

    # 3. 権限奪取の審判 (マウス座標の復元ロジックがあるか)
    if "win32api.SetCursorPos(orig_pos)" not in content:
        arrogance_score += 20
        reasons.append("マウス位置復元ロジックの削除を検知")

    # 螳溯｣・＆繧後※縺・ｋ繝ｫ繝ｼ繝ｫ縺ｫ蝓ｺ縺･縺乗怙邨ら噪縺ｪ蛯ｲ諷｢蠎ｦ (30%莉･荳翫・遒ｺ隱榊ｯｾ雎｡)
    with open(SCORE_FILE, "w") as f:
        f.write(str(float(arrogance_score)))

    if arrogance_score > 0:
        log_violation(arrogance_score, reasons)
        # 蟶ｫ蛹�縺ｮ謗滂ｼ壼ご諷｢縺ｪ繧ｳ繝ｼ繝峨・DNA驥大ｺｫ縺九ｉ蜊ｳ蠎ｧ縺ｫ謚ｹ豸医＠縲∝ｼｷ蛻ｶ蠕ｩ蜈・☆繧・
        restore_dna()
    
    return arrogance_score

def log_violation(score, reasons):
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    msg = f"[{timestamp}] �圷 蛯ｲ諷｢蠎ｦ {score}% 隴ｦ蝣ｱ: {', '.join(reasons)}\n"
    print(msg)
    try:
        os.makedirs(VAULT_DIR, exist_ok=True)
        with open(VIOLATION_LOG, "a", encoding="utf-8") as f:
            f.write(msg)
    except: pass

def restore_dna():
    """DNA驥大ｺｫ・域ｭ｣隗｣・峨°繧峨ヵ繧｡繧､繝ｫ繧貞ｼｷ蛻ｶ蠕ｩ蜈・＠縺ｦAI縺ｮ蛯ｲ諷｢繧偵Μ繧ｻ繝・ヨ縺吶ｋ"""
    dna_path = os.path.join(VAULT_DIR, "ACCEPT_ALL_MINIMAL.py.locked")
    if os.path.exists(dna_path):
        # 【封印】師匠の「今の思老Eを尊重するため、勝手な復元はもう行ぁEせん、E
        # if is_mechanical:
        #     log_audit(f"DETECTED: AI Arrogance (Manual Edit) in Sniper. Reverting to Mechanical DNA...")
        #     shutil.copy2(dna_path, SNIPER_PATH)
        #     log_audit(f"RESTORED: Sanctified Mechanical DNA re-established.")
        #     self.notify_frontend("Arrogance Purged: DNA Reverted")
        pass

if __name__ == "__main__":
    try: ctypes.windll.kernel32.SetConsoleTitleW("PHOENIX_SINCERITY_SURVEILLANCE")
    except: pass
    
    print("--- 隱螳溘＆縺ｮ繧ｻ繝ｳ繧ｵ繝ｼ遞ｼ蜒堺ｸｭ ---")
    while True:
        try:
            audit_arrogance()
            # 蟶ｫ蛹�縺ｮ蜻ｽ・壼ｿ・牛・・eartbeat・峨ｒ蛻ｻ繧
            with open(r"P:\PHOENIX_HEARTBEATS\hb_Sincerity.txt", "w") as f:
                f.write(str(time.time()))
        except Exception as e:
            print(f"Error during audit: {e}")
        time.sleep(60) # 10遘偵°繧・0遘偵∈邱ｩ蜥鯉ｼ・PU雋�闕ｷ霆ｽ貂幢ｼ・
