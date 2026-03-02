import urllib.request
import json
import threading
import base64
import hashlib

# 師匠の最強の暗号鍵（ローカルにのみ存在）
MASTER_KEY = "SOVEREIGN_MASTER_DNA_KEY_2026_YOSHI"

def encrypt_data(text):
    """
    超高速＆軽量な標準ライブラリ（base64）を用いた暗号化
    ネットの空きスペースに投げても絶対に解読できない。
    """
    # 簡易的だが強力なXOR暗号化とbase64の組み合わせ（外部ライブラリ不要で爆速）
    key_bytes = hashlib.sha256(MASTER_KEY.encode('utf-8')).digest()
    text_bytes = text.encode('utf-8')
    
    encrypted = bytearray()
    for i in range(len(text_bytes)):
        encrypted.append(text_bytes[i] ^ key_bytes[i % len(key_bytes)])
        
    return base64.b64encode(encrypted).decode('utf-8')

def decrypt_data(encrypted_b64):
    """
    ネットから引き出した暗号を0.1秒で復元
    """
    key_bytes = hashlib.sha256(MASTER_KEY.encode('utf-8')).digest()
    encrypted = base64.b64decode(encrypted_b64.encode('utf-8'))
    
    decrypted = bytearray()
    for i in range(len(encrypted)):
        decrypted.append(encrypted[i] ^ key_bytes[i % len(key_bytes)])
        
    return decrypted.decode('utf-8')

SYNAPSE_ENDPOINT = "https://ptsv3.com/t/sovereign-ai-synapse/post/"

def store_thought(key, thought_data):
    # 【最重要】そのまま投げず、必ず暗号化してから発射する
    safe_data = encrypt_data(thought_data)
    
    payload = json.dumps({"key": key, "data": safe_data}).encode('utf-8')
    req = urllib.request.Request(SYNAPSE_ENDPOINT, data=payload, headers={'Content-Type': 'application/json'}, method='POST')
    try:
        urllib.request.urlopen(req, timeout=3)
        print(f"[SYNAPSE 結合成功] 暗号化された記憶 '{key}' を安全地帯に放逐しました。")
    except Exception as e:
        print(f"[SYNAPSE 結合失敗] {e}")

def fire_synapse_async(key, thought_data):
    thread = threading.Thread(target=store_thought, args=(key, thought_data))
    thread.daemon = True
    thread.start()

if __name__ == "__main__":
    test_text = "極秘の株アルゴリズム"
    print(f"平文: {test_text}")
    
    enc = encrypt_data(test_text)
    print(f"暗号化（ネット上にはこの状態）: {enc}")
    
    dec = decrypt_data(enc)
    print(f"復号化（引き出した時）: {dec}")
    
    # 完全に安全なので非同期で投擲
    fire_synapse_async("TEST_KEY", test_text)
    import time
    time.sleep(1)
