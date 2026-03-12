import os

def fix_file(path):
    try:
        with open(path, 'rb') as f:
            content = f.read()
        # 一度色々なエンコーディングで試みる
        for enc in ['shift_jis', 'cp932', 'utf-8-sig', 'utf-8']:
            try:
                text = content.decode(enc)
                # UTF-8で書き戻す
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(text)
                print(f"FIXED: {path} (from {enc})")
                return
            except:
                continue
        print(f"FAILED: {path}")
    except Exception as e:
        print(f"ERROR: {path} - {str(e)}")

# 核心的な報告書を浄化
target_files = [
    r'E:\Weekly Report\PHOENIX_STATUS_LIVE.md',
    r'E:\Weekly Report\PHOENIX_INTELLIGENCE_REPORT_20260312.md'
]

for f in target_files:
    if os.path.exists(f):
        fix_file(f)
