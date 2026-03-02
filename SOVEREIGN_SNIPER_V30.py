import pywinauto
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')

def final_sniper_v30():
    print("Sovereign Sniper v30.0 (Deep Visual Search) 起動...")
    # ターゲット候補（真名・内部名）
    target_names = ["Run", "Always run", "Allow", "Accept", "AcceptAll", "Execute", "実行"]
    
    try:
        desktop = pywinauto.Desktop(backend="uia")
        # デスクトップ全体からボタンを直接探す
        all_buttons = desktop.descendants(control_type="Button")
        
        found = False
        for btn in all_buttons:
            try:
                name = btn.window_text()
                if any(t in name for t in target_names):
                    rect = btn.rectangle()
                    print(f"!!! ターゲット捕捉 !!! Name: '{name}' | Coord: ({rect.left}, {rect.top})")
                    btn.click_input()
                    print(f"狙撃成功: {name}")
                    found = True
            except: continue
        
        if not found:
            print("視認できるターゲットが見つかりません。")
            
    except Exception as e:
        print(f"エラー: {e}")

if __name__ == "__main__":
    final_sniper_v30()
