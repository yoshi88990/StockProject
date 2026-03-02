import urllib.request
import json

# JSONBin(完全無料/無登録のAPI)を使って、思考やDNA（ルール）をネットの空き領域に分散記憶させる
# これによりローカルPCの容量や負荷ゼロで知恵を引き出せる

def save_memory_to_synapse(memory_key, memory_content):
    url = "https://jsonbox.io/box_sovereign_ai_synapse_01"
    
    data = {"key": memory_key, "content": memory_content}
    req_data = json.dumps(data).encode('utf-8')
    
    req = urllib.request.Request(url, data=req_data, headers={'Content-Type': 'application/json'})
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode())
            print(f"✅ シナプス（記録保管庫）への接続と保存に成功しました: {result['_id']}")
            return result
    except Exception as e:
        print(f"❌ シナプス接続失敗: {e}")

def load_memory_from_synapse():
    url = "https://jsonbox.io/box_sovereign_ai_synapse_01"
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            print("【ネットのシナプスから取得した記憶】")
            for item in data[:3]: # 最新の3件
                print(f"- {item.get('key')}: {item.get('content')}")
    except Exception as e:
        print(f"❌ シナプス読み取り失敗: {e}")

if __name__ == "__main__":
    print("分散ネットワーク（シナプス）への接続テストを開始します...")
    save_memory_to_synapse("THE_DNA", "思考の加速、待機の廃止、10秒に1回だけ撃つ完全沈黙のスナイパー")
    load_memory_from_synapse()
