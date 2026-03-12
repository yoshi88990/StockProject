import os

def force_utf8(directory):
    print(f"Starting gritty encoding fix in: {directory}")
    for root, dirs, files in os.walk(directory):
        if '.git' in root:
            continue
        for file in files:
            if file.endswith(('.md', '.py', '.bat', '.txt', '.json', '.html', '.css', '.vbs', '.ps1')):
                path = os.path.join(root, file)
                try:
                    # Try to detect current encoding
                    with open(path, 'rb') as f:
                        raw = f.read()
                    
                    if not raw:
                        continue
                        
                    content = None
                    # Try UTF-8 first
                    try:
                        content = raw.decode('utf-8')
                        print(f"ALREADY UTF-8: {path}")
                    except UnicodeDecodeError:
                        # Try Shift-JIS
                        try:
                            content = raw.decode('shift_jis')
                            print(f"CONVERTING SJIS -> UTF-8: {path}")
                        except UnicodeDecodeError:
                            # Try CP932
                            try:
                                content = raw.decode('cp932')
                                print(f"CONVERTING CP932 -> UTF-8: {path}")
                            except UnicodeDecodeError:
                                print(f"FAILED TO DECODE: {path}")
                                continue
                    
                    if content:
                        # Normalize line endings to Windows (CRLF) and write as UTF-8
                        content = content.replace('\r\n', '\n').replace('\n', '\r\n')
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(content)
                            
                except Exception as e:
                    print(f"ERROR processing {path}: {e}")

# Fix both locations
force_utf8(r'E:\Weekly Report')
force_utf8(r'E:\StockProject')
