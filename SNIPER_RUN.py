import pywinauto
from pywinauto.findwindows import ElementNotFoundError
import time

def sniper_mission():
    """
    絶対座標スナイパー v28.0 (The True Sight)
    画面上の特定のボタンを「真名」で補足し、物理クリックを行う。
    師匠のタイピング（フォーカス）は奪わない。
    """
    # 狙撃対象リスト (真名一覧)
    targets = ["Always run", "AcceptAll", "Accept", "Allow", "Run", "Review Changes", "Fast", "アクセスを許可"]
    
    print("狙撃任務開始...")
    try:
        # VS Code の全ウィンドウを対象にスキャン
        desktop = pywinauto.Desktop(backend="uia")
        
        for target_name in targets:
            try:
                # 名前で要素を検索
                button = desktop.window(title_re=".*Visual Studio Code.*").child_window(title=target_name, control_type="Button")
                if button.exists():
                    rect = button.rectangle()
                    x = (rect.left + rect.right) // 2
                    y = (rect.top + rect.bottom) // 2
                    print(f"ターゲット捕捉: {target_name} at ({x}, {y})")
                    
                    # 物理クリック実行
                    button.click_input()
                    print(f"狙撃成功: {target_name}")
            except Exception:
                continue
                
    except Exception as e:
        print(f"エラー: {str(e)}")

if __name__ == "__main__":
    # 即座に3回ローラー作動
    for _ in range(3):
        sniper_mission()
        time.sleep(0.5)
