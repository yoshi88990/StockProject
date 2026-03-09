import pyperclip
import time
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from colorama import init, Fore, Style
from IPO_DNA_ANALYZER import IPODnaAnalyzer

init(autoreset=True)

# 文字化け対策
try:
    if sys.stdout.encoding != 'utf-8':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
except: pass

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    analyzer = IPODnaAnalyzer()
    print(Fore.CYAN + Style.BRIGHT + "┌──────────────────────────────────────────────┐")
    print(Fore.CYAN + "│ " + Fore.YELLOW + Style.BRIGHT + " 👁️ DNA_SNIPER v2.5 [ULTIMATE OMNI-EYE] " + Fore.CYAN + "│")
    print(Fore.CYAN + "└──────────────────────────────────────────────┘")
    print(Fore.WHITE + " -> [全知全能] 四季報・目論見書をスキャン中...")

    last_clipboard = ""

    while True:
        try:
            # 師匠の命：前後の空白を削除し、純粋な中身だけを見る
            current_clipboard = pyperclip.paste().strip()
            
            if current_clipboard != last_clipboard and len(current_clipboard) > 10:
                text = current_clipboard.replace('\n', ' ')
                
                # --- 解析アルゴリズム ---
                owner_pattern = r'([^ 　\d\(]{2,8})(?:[ 　]*)(?:\(社長|\(代表|\(会長|代表取締役|創業者|筆頭株主)'
                found_owners = re.findall(owner_pattern, text)
                holdings = re.findall(r'(?:株式会社|有限会社)([A-Z]{2,10}|[ァ-ン]{2,10})', text)
                
                vc_found = []
                for kw in analyzer.vc_keywords:
                    vc_found.extend(re.findall(rf'([^ 　\d]{{2,15}}{kw}[^ 　\d]*)', text))
                
                # 師匠の命：何一つ「因果」が見つからない場合は、ピクピク動かず沈黙を貫く。
                if any([found_owners, holdings, vc_found]):
                    print(Fore.CYAN + "\n" + "-" * 48)
                    print(Fore.YELLOW + Style.BRIGHT + f" [ 👁️  DNA_SNIPER v2.7 資産DNA検知 ] - {time.strftime('%H:%M:%S')}")
                    
                    vc_pressure = "LOW"
                    if len(vc_found) > 3: vc_pressure = "HIGH 🚨"
                    elif vc_found: vc_pressure = "MEDIUM ⚠️"
                    
                    dna_type = "👔 雇われ・一般系"
                    color = Fore.WHITE
                    if (found_owners or holdings) and not vc_found:
                        dna_type = "🐶 理想の創業者ワンマンDNA"
                        color = Fore.GREEN
                    elif (found_owners or holdings) and vc_found:
                        dna_type = "⚔️ 攻防混在（出口戦略を要警戒）"
                        color = Fore.YELLOW
                    elif vc_found:
                        dna_type = "🏦 投資家主導（イグジット狙い）"
                        color = Fore.RED

                    print(f" > 判定: {color}{Style.BRIGHT}{dna_type}")
                    print(f" > 需給: {Fore.CYAN if vc_pressure=='LOW' else (Fore.YELLOW if 'MEDIUM' in vc_pressure else Fore.RED)}{vc_pressure}")
                    
                    if found_owners: print(Fore.GREEN + f" > 創業者: {', '.join(set(found_owners))}")
                    if holdings: print(Fore.GREEN + f" > 資産管理: {', '.join(set(holdings))}")
                    
                    # --- 保存 ---
                    try:
                        stash_dir = r"C:\Users\kanku\OneDrive\Weekly report\Phoenix_Protocol\INTELLIGENCE_STASH"
                        if not os.path.exists(stash_dir): os.makedirs(stash_dir)
                        safe_name = "".join(x for x in text[:10] if x.isalnum())
                        filename = f"SNIPE_{int(time.time())}_{safe_name}.json"
                        with open(os.path.join(stash_dir, filename), "w", encoding="utf-8") as f:
                            import json
                            json.dump({
                                "time": time.strftime('%Y-%m-%d %H:%M:%S'),
                                "dna": dna_type, "vc_pressure": vc_pressure,
                                "owners": found_owners, "holdings": holdings, "raw": text[:1000]
                            }, f, ensure_ascii=False, indent=2)
                        print(Fore.CYAN + " (資産アーカイブ同期完了 / 待機中...)")
                    except: pass

                last_clipboard = current_clipboard
            
            time.sleep(1.5) # 師匠の命：急がず、静かに監視

        except KeyboardInterrupt: break
        except Exception: time.sleep(1)

if __name__ == "__main__":
    main()
