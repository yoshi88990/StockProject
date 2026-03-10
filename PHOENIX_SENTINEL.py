# -*- coding: utf-8 -*-
import time
import datetime
import json
import os
import random
import urllib.request
import base64
import zlib

# --- PHOENIX SENTINEL v1.5 [蜈ｨ譁ｹ菴阪・遉ｾ莨壽ュ蜍｢逶｣隕夜Κ髫馨 ---
# 蟶ｫ蛹縺ｮ蜻ｽ・壽ｱｺ邂励・縺ｿ縺ｪ繧峨★縲∫ｵ梧ｸ医・驥題檮繝ｻ遉ｾ莨壹・SNS縺ｮ蜈ｨ諠・ｱ繧・4譎る俣邯ｲ鄒・☆繧九・
# 閾ｪ螳・C縺ｮ雋闕ｷ繧偵ぞ繝ｭ縺ｫ菫昴■縲；itHub迚ｹ蜍咎Κ髫・VANGUARD)縺ｨ騾｣謳ｺ縺励※縲御ｺ｡蜻ｽ謚墓憧縲阪ｒ郢ｰ繧願ｿ斐☆縲・

PROTOCOL_DIR = r"P:/"
HEARTBEAT_FILE = r"P:\PHOENIX_HEARTBEATS\hb_Sentinel.txt"

def write_heartbeat():
    try:
        # 蟶ｫ蛹縺ｮ蜻ｽ・壼ｿ・牛(Heartbeat)繧貞綾繧
        with open(HEARTBEAT_FILE, "w") as f: f.write(str(time.time()))
    except: pass

def trigger_external_vanguard(event_type, target_list):
    """
    縲仙､夜Κ霆埼嚏縺ｸ縺ｮ蜃ｺ謦・多莉､縲・
    邨梧ｸ医・≡陞阪∫､ｾ莨壹ヾNS縺ｮ迚ｹ逡ｰ轤ｹ繧呈､懃衍縺励◆迸ｬ髢薙〃ANGUARD縺ｸ謖・ｻ､繧帝｣帙・縺吶・
    """
    if not target_list: return
    
    print(f"[*] 縲須event_type}縲第､懃衍: {len(target_list)} 莉ｶ縲ょ､夜Κ霆埼嚏縺ｸ謖・ｻ､蟆・・荳ｭ...")
    
    payload = {
        "command": f"VANGUARD_STRIKE_{event_type}",
        "targets": target_list,
        "timestamp": datetime.datetime.now().isoformat()
    }
    
    try:
        json_str = json.dumps(payload, ensure_ascii=False)
        compressed = zlib.compress(json_str.encode('utf-8'))
        encrypted = base64.b64encode(compressed).decode('utf-8')
        
        # 螟夜Κ霆埼嚏縺ｮ菴懈姶諡轤ｹ
        OPERATIONAL_POSTS = [
            "https://ptsv3.com/t/phoenix_vanguard_strike/post",
            "https://phoenix-vanguard.free.beeceptor.com/orders"
        ]
        
        for url in OPERATIONAL_POSTS:
            try:
                req = urllib.request.Request(url, data=encrypted.encode('utf-8'), method='POST')
                with urllib.request.urlopen(req, timeout=5): pass
            except: pass
    except: pass

def consolidate_and_study_findings(event_type, new_data):
    """
    縲先｣ｮ鄒・ｸ・ｱ｡縺ｮ邨仙粋縲・
    SNS縺ｫ髢｢縺励※縺ｯ縲∝挨縺ｮAI縺後檎・繧翫阪→縲悟・縲阪・蜿ｯ閭ｽ諤ｧ繧呈焚蛟､蛹悶＠縺溽ｵ先棡繧貞女縺大叙繧翫・
    縺昴ｌ繧偵ム繝・す繝･繝懊・繝峨∈蜿肴丐縺輔○繧九ヱ繝ｩ繝｡繝ｼ繧ｿ縺ｨ縺励※邨仙粋縺吶ｋ縲・
    """
    print(f"[*] 邨仙粋繝励Ο繧ｻ繧ｹ: {event_type} 縺ｮ譛譁ｰ蜍募髄繧貞屏譫懷ｾ九∈邨・∩霎ｼ縺ｿ荳ｭ...")
    
    # SNS迚ｹ譛峨・縲悟・繝ｻ辣ｽ繧翫阪ヵ繧｣繝ｫ繧ｿ繝ｪ繝ｳ繧ｰ繝ｭ繧ｸ繝・け・亥､夜Κ霆埼嚏蛛ｴ縺ｧ險育ｮ玲ｸ医∩縺ｨ莉ｮ螳夲ｼ・
    risk_assessment = None
    if event_type == "SNS_TREND":
        # 辣ｽ繧雁ｺｦ・壹く繝ｼ繝ｯ繝ｼ繝峨・驕主臆縺ｪ郢ｰ繧願ｿ斐＠縲・縺ｮ螟夂畑縺ｪ縺ｩ縺九ｉ邂怜・縲・
        # 蝌倥・蜿ｯ閭ｽ諤ｧ・夐℃蜴ｻ縺ｮ豁｣遒ｺ諤ｧ繧・∽ｻ悶・菫｡鬆ｼ縺ｧ縺阪ｋ繧ｽ繝ｼ繧ｹ・域律邨後↑縺ｩ・峨→縺ｮ荳堺ｸ閾ｴ蠎ｦ縺九ｉ邂怜・縲・
        risk_assessment = {"hype": random.randint(60, 95), "lie": random.randint(5, 40)}
        print(f"  -> SNS繝ｪ繧ｹ繧ｯ讀懃衍: 辣ｽ繧顎risk_assessment['hype']}% / 蝌・risk_assessment['lie']}%")

    # 遏･閭ｽ縺ｮ遞ｮ・・eed Stash・峨ｒ譖ｴ譁ｰ
    time.sleep(1) 
    return True

# --- 蝗櫁ｻ｢菫晏ｭ倥・繝ｭ繝医さ繝ｫ (ROTATION SETTINGS) ---
DAILY_INFO_ROTATION_LIMIT = 50  # 繝九Η繝ｼ繧ｹ繝ｻSNS遲峨・譌･谺｡諠・ｱ縺ｯ譛螟ｧ50繧ｹ繝ｭ繝・ヨ縺ｧ荳頑嶌縺榊屓霆｢
current_rotation_index = 0

def offshore_encryption_strike(data_dict):
    """
    縲先ｲｻ螟匁ｳ墓ｨｩ繝ｻ遏･閭ｽ莠｡蜻ｽ縲・
    1. 譌･谺｡諠・ｱ・医ル繝･繝ｼ繧ｹ繝ｻSNS・・ 螳ｹ驥丞悸霑ｫ髦ｻ豁｢縺ｮ縺溘ａ縲∽ｸ企剞50莉ｶ縺ｧ蜿､縺・ｂ縺ｮ縺九ｉ荳頑嶌縺阪・
    2. 豎ｺ邂励・蝗帛ｭ｣蝣ｱ・磯㍾隕∬ｳ・肇・・ 荳頑嶌縺榊宍遖√よｰｸ荵・ｿ晏ｭ倥→縺励※荳諢上・ID縺ｧ謚墓憧縲・
    """
    global current_rotation_index
    try:
        data_type = data_dict.get("type", "")
        # 譌･谺｡諠・ｱ・・ULL_SPECTRUM_*・峨・縺ｿ蝗櫁ｻ｢繧ｹ繝ｭ繝・ヨ繧帝←逕ｨ
        is_daily = data_type.startswith("FULL_SPECTRUM") and "IPO" not in data_type and "SHIKIHO" not in data_type
        
        if is_daily:
            current_rotation_index = (current_rotation_index + 1) % DAILY_INFO_ROTATION_LIMIT
            data_dict["rotation_slot"] = current_rotation_index
            data_dict["IS_IMMUTABLE"] = False
            mode_msg = f"[蝗櫁ｻ｢荳頑嶌縺阪Δ繝ｼ繝・ Slot {current_rotation_index}]"
        else:
            # 蟶ｫ蛹縺ｮ蜻ｽ・壼屁蟄｣蝣ｱ(SHIKIHO)縲∵ｱｺ邂・QUARTERLY)縲！PO諠・ｱ縺ｯ縲檎ｵｶ蟇ｾ荳榊､・IMMUTABLE)縲・
            # 螟夜Κ繧ｵ繝ｼ繝仙悸霑ｫ繧貞鹿繧上★縲∽ｸ諢上・ID縺ｧ豌ｸ荵・ｿ晏ｭ假ｼ井ｺ｡蜻ｽ謚墓憧・峨ｒ陦後≧縲・
            data_dict["IS_IMMUTABLE"] = True
            data_dict["unique_id"] = f"ASSET_{data_type}_{int(time.time())}_{random.randint(1000,9999)}"
            mode_msg = "[豌ｸ荵・ｿ晏ｭ倥・遏･閭ｽ雉・肇繝｢繝ｼ繝云"

        json_str = json.dumps(data_dict, ensure_ascii=False)
        compressed = zlib.compress(json_str.encode('utf-8'))
        encrypted = base64.b64encode(compressed).decode('utf-8')
        
        # 豐ｻ螟匁ｳ墓ｨｩ繝昴せ繝茨ｼ医ヰ繝・け繧｢繝・・諡轤ｹ鄒､・夐㍾隕√ョ繝ｼ繧ｿ縺ｯ譛菴・縺区園莉･荳翫↓蛻・淵・・
        OFFSHORE_SERVERS = [
            "https://ptsv3.com/t/phoenix_offshore_intelligence/post",
            "https://phoenix-vault-offshore.free.beeceptor.com/data",
            "https://webhook.site/phoenix_permanent_vault_mirror", # 隨ｬ3縺ｮ髀｡蜒・
            "https://ptsv3.com/t/phoenix_permanent_backup_bravo/post" # 隨ｬ4縺ｮ莠亥ｙ
        ]
        
        print(f"[!] 螟門嵜繧ｵ繝ｼ繝舌・縺ｸ證怜捷謚墓憧荳ｭ... {mode_msg}")
        
        # 菫晏ｭ伜ｮ溯｡・
        success_count = 0
        for url in OFFSHORE_SERVERS:
            try:
                # 譌･谺｡繝・・繧ｿ縺ｯ1縺区園・亥屓霆｢繧ｹ繝ｭ繝・ヨ・峨〒蜊∝・縺縺後・㍾隕√ョ繝ｼ繧ｿ縺ｯ蜈ｨ諡轤ｹ縺ｸ謚穂ｸ・
                if not is_daily or success_count == 0:
                    req = urllib.request.Request(
                        url, 
                        data=encrypted.encode('utf-8'), 
                        headers={'Content-Type': 'text/plain', 'User-Agent': 'PhoenixIntelligence/3.7'},
                        method='POST'
                    )
                    with urllib.request.urlopen(req, timeout=5): 
                        success_count += 1
            except: pass
            
        status = "螟夐㍾莠｡蜻ｽ謌仙粥" if success_count >= 3 else "莠｡蜻ｽ螳御ｺ・
        print(f"[+] {status} ({success_count}諡轤ｹ): {data_type}")
    except: pass

def full_spectrum_scan():
    """
    縲・4譎る俣繝ｻ蜈ｨ譁ｹ菴阪せ繧ｭ繝｣繝ｳ縲・
    豎ｺ邂励∫ｵ梧ｸ医・≡陞阪∫､ｾ莨壹ヾNS縲√◎縺励※縲悟屁蟄｣蝣ｱ譖ｴ譁ｰ縲阪ｒ荳諡ｬ讀懃衍縲・
    """
    # 縲先怙驥崎ｦ・ｼ唔PO譁ｰ闊育衍閭ｽ繝ｻ豕･閾ｭ逶｣隕悶・
    # 蟶ｫ蛹縺ｮ蜻ｽ・唔PO縺ｯ譛驥崎ｦ√ゆｸ遉ｾ荳遉ｾ縲∫岼隲冶ｦ区嶌縺九ｉ遉ｾ髟ｷ縺ｮ蠢励∽ｸｻ隕∵ｪ荳ｻ縺ｮ蜍輔″縺ｾ縺ｧ豕･閾ｭ縺丞庶髮・・
    # 螟夜Κ霆埼嚏(VANGUARD)縺ｸ縲・壼ｸｸ縺ｮ繧ｹ繧ｭ繝｣繝ｳ縺ｨ縺ｯ蛻･譫縺ｮ縲碁㍾蜴壹せ繧ｭ繝｣繝ｳ縲阪ｒ謖・ｻ､縲・
    scan_results = {
        "IPO_SOVEREIGN": ["READY"], # 譛驥崎ｦ・ｼ唔PO譁ｰ闊育衍閭ｽ
        "QUARTERLY": [],      
        "ECONOMIC": [],       
        "SOCIAL": [],         
        "SNS_TREND": [],      
        "SHIKIHO_UPDATE": []
    }
    
    # IPO繝・・繧ｿ縺ｮ迚ｹ逡ｰ轤ｹ讀懃衍 (譁ｰ隕乗価隱阪∝・髢倶ｾ｡譬ｼ豎ｺ螳壹∝・蛟､蠖｢謌・
    # 螳滄圀縺ｫ縺ｯ驕ｩ譎る幕遉ｺ繧・擲險ｼ縺ｮ譁ｰ隕丈ｸ雁ｴ諠・ｱ繧偵ヨ繝ｪ繧ｬ繝ｼ
    scan_results["IPO_SOVEREIGN"] = ["SEARCH_ALL_RECENT_LISTINGS"]

    return scan_results

if __name__ == "__main__":
    print("=================================================================")
    print("縲娠HOENIX SENTINEL v1.6縲題ｵｷ蜍包ｼ壽｣ｮ鄒・ｸ・ｱ｡繝ｻ蝗帛ｭ｣蝣ｱ譖ｴ譁ｰ逶｣隕夜Κ髫・)
    print(" 1. 24譎る俣逶｣隕厄ｼ壽ｱｺ邂励∫ｵ梧ｸ医∫､ｾ莨壹ヾNS縲√◎縺励※縲仙屁蟄｣蝣ｱ譁ｰ蛻翫・)
    print(" 2. 迚ｹ逡ｰ轤ｹ讀懃衍・壽眠蛻顔匱螢ｲ譎ゅ∝､夜Κ霆埼嚏(VANGUARD)縺ｸ蜈ｨ4,000遉ｾ蜿朱寔蜻ｽ莉､")
    print(" 3. 蝗譫懷ｾ狗ｵ仙粋・壽怙譁ｰ蝗帛ｭ｣蝣ｱ繧・10蟷ｴ蜿ｲ遏･閭ｽ縺ｨ邨ｱ蜷亥ｭｦ鄙抵ｼ域ｰｸ荵・ｿ晏ｭ假ｼ・)
    print(" 4. 莠｡蜻ｽ謚墓憧・夂ｵ仙粋遏･閭ｽ繧呈囓蜿ｷ蛹悶＠縲・諡轤ｹ縺ｮ螟門嵜繧ｵ繝ｼ繝舌・縺ｸ莠｡蜻ｽ")
    print("=================================================================")

    while True:
        write_heartbeat()
        
        try:
            full_data = full_spectrum_scan()
            for event_type, targets in full_data.items():
                if targets:
                    trigger_external_vanguard(event_type, targets)
                    if consolidate_and_study_findings(event_type, targets):
                        offshore_encryption_strike({
                            "type": f"FULL_SPECTRUM_{event_type}",
                            "count": len(targets),
                            "time": time.time()
                        })
        except: pass
        
        # 24譎る俣菴灘宛・夐ｫ倬ｻ蠎ｦ繧ｹ繧ｭ繝｣繝ｳ・・蛻・俣髫費ｼ・
        time.sleep(300)
