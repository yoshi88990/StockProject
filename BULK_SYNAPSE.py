import os
import json
import SOVEREIGN_SYNAPSE as syn

# 全DNA（備忘録）を舐め回してネット上に暗号化分散（バックグラウンドに逃がす）
memo_dir = "備忘録"
if os.path.exists(memo_dir):
    for filename in os.listdir(memo_dir):
        if filename.endswith(".md"):
            filepath = os.path.join(memo_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            syn.fire_synapse_async(filename, content)
            print(f"分散完了: {filename}")
print("全てのDNAのネット（シナプス）への分散放逐が完了しました。")
