  [ 泥臭収集 ] ██░░░░░░░░░░░░░ 15.6%import pyperclip
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

    protocol_dir = r"C:\Users\kanku\OneDrive\Weekly report\Phoenix_Protocol"
    
    # 師匠の命：引数からターゲットコードを取得
    target_code = ""
    if len(sys.argv) > 1:
        target_code = sys.argv[1].strip()
    
    # 師匠の命：資産計算は「外部軍隊」の総結集
    ipo_collected = 0
    for root, dirs, files in os.walk(protocol_dir):
        ipo_collected += len([f for f in files if f.endswith('.json')])
    
    ipo_total = 45
    pct = (ipo_collected / ipo_total) * 100 if ipo_total > 0 else 0
    if pct > 100: pct = 100.0
    
    bar_len = 15
    filled = int(bar_len * pct / 100)
    bar = Fore.GREEN + "█" * filled + Fore.WHITE + "░" * (bar_len - filled)

    # 師匠の命：タイトル -> 進捗率 -> 検索窓 (黄金の三段構成)
    clear_console()
    print(Fore.CYAN + Style.BRIGHT + "┌──────────────────────────────────────────────┐")
    print(Fore.CYAN + "│ " + Fore.YELLOW + Style.BRIGHT + " 👁️ DNA_SNIPER v3.7 [TARGETED SENTRY]   " + Fore.CYAN + "│")
    print(Fore.CYAN + f"│ [ 進捗: {bar} {pct:.1f}% ({ipo_collected}/{ipo_total}) ] " + Fore.CYAN + "│")
    print(Fore.CYAN + "├──────────────────────────────────────────────┤")
    if target_code:
        display_target = f"狙撃対象: [ {target_code} ]"
    else:
        display_target = "狙撃対象: [ 全方位・自動検知 ]"
    
    # センター揃えの計算
    padding = (44 - len(display_target.encode('shift_jis', errors='ignore'))) // 2
    if padding < 0: padding = 0
    print(Fore.CYAN + "│ " + Fore.WHITE + " " * padding + display_target + " " * (44 - padding - len(display_target.encode('shift_jis', errors='ignore'))) + Fore.CYAN + "│")
    print(Fore.CYAN + "└──────────────────────────────────────────────┘")
    print(Fore.LIGHTBLACK_EX + f"  >> {'特定コードの巡回中...' if target_code else '部隊は沈黙し、師匠のスナイプを待機中...'}")

    last_clipboard = ""

    while True:
        try:
            current_clipboard = pyperclip.paste().strip()
            
            if current_clipboard != last_clipboard and len(current_clipboard) > 10:
                text = current_clipboard.replace('\n', ' ')
                
                # 簡易DNA解析ロジック
                # 実際の IPODnaAnalyzer はもっと複雑なリストを受け取るが、
                # ここではコピペされたテキストから「オーナー」「VC」の断片を抽出
                owner_pattern = r'([^ 　\d\(]{2,8})(?:[ 　]*)(?:\(社長|\(代表|\(会長|代表取締役|創業者|筆頭株主)'
                found_owners = re.findall(owner_pattern, text)
                holdings = re.findall(r'(?:株式会社|有限会社)([A-Z]{2,10}|[ァ-ン]{2,10})', text)
                
                vc_found = []
                for kw in analyzer.vc_keywords:
                    vc_found.extend(re.findall(rf'([^ 　\d]{{2,15}}{kw}[^ 　\d]*)', text))
                
                if any([found_owners, holdings, vc_found]):
                    print(Fore.CYAN + "\n" + "-" * 48)
                    print(Fore.YELLOW + Style.BRIGHT + f" [ 👁️  DNA検知 ] - {time.strftime('%H:%M:%S')}")
                    if target_code:
                        print(Fore.WHITE + f" [ 標的コード: {target_code} ]")
                    
                    vc_pressure = "LOW"
                    if len(vc_found) > 3: vc_pressure = "HIGH 🚨"
                    elif vc_found: vc_pressure = "MEDIUM ⚠️"
                    
                    dna_type = "👔 雇われ・一般系"
                    color = Style.NORMAL
                    if (found_owners or holdings) and not vc_found:
                        dna_type = "🐶 理想の創業者ワンマンDNA"
                        color = Fore.GREEN + Style.BRIGHT
                    elif (found_owners or holdings) and vc_found:
                        dna_type = "⚔️ 攻防混在（出口戦略を要警戒）"
                        color = Fore.YELLOW + Style.BRIGHT
                    elif vc_found:
                        dna_type = "🏦 投資家主導（イグジット狙い）"
                        color = Fore.RED + Style.BRIGHT

                    print(f" > 判定: {color}{dna_type}")
                    print(f" > 需給: {Fore.CYAN if vc_pressure=='LOW' else (Fore.YELLOW if 'MEDIUM' in vc_pressure else Fore.RED)}{vc_pressure}")
                    
                    if found_owners: print(Fore.GREEN + f" > 創業者: {', '.join(set(found_owners))}")
                    if holdings: print(Fore.GREEN + f" > 資産管理: {', '.join(set(holdings))}")
                    
                    try:
                        stash_dir = os.path.join(protocol_dir, "INTELLIGENCE_STASH")
                        if not os.path.exists(stash_dir): os.makedirs(stash_dir)
                        # ファイル名にコードを付与して整理しやすく
                        prefix = f"{target_code}_" if target_code else ""
                        safe_name = "".join(x for x in text[:10] if x.isalnum())
                        filename = f"SNIPE_{prefix}{int(time.time())}_{safe_name}.json"
                        
                        with open(os.path.join(stash_dir, filename), "w", encoding="utf-8") as f:
                            import json
                            json.dump({
                                "code": target_code,
                                "time": time.strftime('%Y-%m-%d %H:%M:%S'),
                                "dna": dna_type, "vc_pressure": vc_pressure,
                                "owners": found_owners, "holdings": holdings, "raw": text[:1000]
                            }, f, ensure_ascii=False, indent=2)
                        print(Fore.CYAN + f" (知能 '{filename}' へのアーカイブ完了)")
                    except Exception as e:
                        print(Fore.RED + f" (保存エラー: {e})")

                last_clipboard = current_clipboard
            
            time.sleep(1.5)

        except KeyboardInterrupt: break
        except Exception: time.sleep(1.5)

        except KeyboardInterrupt: break
        except Exception: time.sleep(1)

if __name__ == "__main__":
    main()
