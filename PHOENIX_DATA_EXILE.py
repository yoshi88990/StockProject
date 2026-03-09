import os
import json
import zlib
import base64
import time
import glob

# --- PHOENIX DATA CLOUD VANGUARD: EXPORT PROTOCOL ---
# 1. ローカルで収集した膨大な歴史（JSON）を一つに統合。
# 2. zlib + Base64 で極限まで圧縮・暗号化（Payload化）。
# 3. 外部の「外国サーバー（GitHub/Gist等）」へ亡命（保存）させるための準備。

SOURCE_DIR = r"C:\StockProject\PHOENIX_CHRONICLE_10Y\DATA"
# 【生命線】クラウド同期されるOneDriveフォルダを優先
ONEDRIVE_PATH = os.path.join(os.environ["USERPROFILE"], "OneDrive", "Weekly report", "Phoenix_Protocol", "DATA_EXILE_VAULT")
EXPORT_DIR = ONEDRIVE_PATH if os.path.exists(os.path.dirname(ONEDRIVE_PATH)) else r"C:\StockProject\PHOENIX_EXPORTS"
LOG_FILE = r"C:\StockProject\export_history.txt"

def secure_exile_payload_chunked(chunk_size=1000):
    """
    【生命線の防護】メモリ爆発を避け、1000件ごとに小分けにして亡命（エクスポート）させる。
    """
    if not os.path.exists(EXPORT_DIR):
        os.makedirs(EXPORT_DIR)

    # 1. 亡命すべきファイルリストを取得
    data_files = sorted(glob.glob(os.path.join(SOURCE_DIR, "*.json")))
    if not data_files:
        print("[-] 亡命命令：新着知識はまだ届いていません。保持を継続します。")
        return

    # すでに亡命済みの分を除外するために、進捗を記録（簡易版）
    total_files = len(data_files)
    print(f"[+] 知識の生命線を監査：全 {total_files} 件。{chunk_size} 件ずつ分断亡命を開始。")

    for i in range(0, total_files, chunk_size):
        chunk = data_files[i : i + chunk_size]
        all_knowledge = {}
        
        # 2. 分断結合（メモリ消費を一定に保つ）
        for f_path in chunk:
            try:
                with open(f_path, "r", encoding="utf-8") as f:
                    core_data = json.load(f)
                    code = core_data.get("code")
                    if code:
                        if code not in all_knowledge: all_knowledge[code] = []
                        all_knowledge[code].append(core_data)
            except: continue

        if not all_knowledge: continue

        # 3. 圧縮・暗号化 (zlib + Base64)
        try:
            raw_payload = json.dumps(all_knowledge, ensure_ascii=False)
            compressed = zlib.compress(raw_payload.encode('utf-8'))
            encrypted = base64.b64encode(compressed).decode('utf-8')

            # 4. 亡命ファイル生成（一時ファイルを作成してからリネームし、原子性を確保）
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            export_filename = f"PHOENIX_CHUNK_{i//chunk_size + 1}_{timestamp}.dat"
            export_path = os.path.join(EXPORT_DIR, export_filename)
            temp_path = export_path + ".tmp"
            
            with open(temp_path, "w", encoding="utf-8") as f:
                f.write(encrypted)
            
            os.replace(temp_path, export_path) # 原子的なリネーム

            msg = f"[{time.strftime('%H:%M:%S')}] 生命線の分断亡命成功：{export_filename} ({len(chunk)}件格納)"
            print(msg)
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(msg + "\n")
                
        except Exception as e:
            print(f"[!] 生命線の切断を検知：{e}")
            if os.path.exists(temp_path): os.remove(temp_path)

    return EXPORT_DIR

if __name__ == "__main__":
    print("--- [鳳凰・知識の生命線：分断亡命プロトコル] 起動 ---")
    secure_exile_payload_chunked(chunk_size=1000)
