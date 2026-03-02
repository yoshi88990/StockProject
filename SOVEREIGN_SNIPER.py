import pywinauto
import time
import keyboard
import sys

sys.stdout.reconfigure(encoding='utf-8')

def sentinel_observer_v69():
    """
    Sentinel Observer v69.0 (The F12 Trigger)
    - 師匠の「座標は不要。出たら F12 を押せ」という戦略的転換を採用。
    - UIスキャンでターゲット（Run/Accept）を検知した瞬間に F12 ホットキーを仮想打鍵する。
    - 物理的な座標計算に頼らず、師匠が設定した「F12（必殺連撃）」を自動で引き出す。
    """
    print("センチネル監視システム v69.0 起動... (F12 自動トリガー方式)")
    
    keywords = ["always run", "run", "accept", "run command?"]
    
    try:
        desktop = pywinauto.Desktop(backend="uia")
        
        while True:
            # ESCで監視停止
            if keyboard.is_pressed('esc'): break
            
            try:
                found = False
                for win in desktop.windows():
                    # VS Code またはそれに関連する窓を監視
                    if "Visual Studio Code" in win.window_text() or "Stock" in win.window_text() or not win.window_text():
                        # ウィンドウ内または通知内のテキストをスキャン
                        # 文言ベースの判定
                        try:
                            # ボタン要素を直接探す
                            all_btns = win.descendants(control_type="Button")
                            for btn in all_btns:
                                name = btn.window_text().lower()
                                if name and any(k in name for k in keywords):
                                    found = True
                                    target_name = name
                                    break
                            
                            # またはダイアログ内のテキスト
                            if not found:
                                all_texts = win.descendants(control_type="Text")
                                for t in all_texts:
                                    t_txt = t.window_text().lower()
                                    if any(k in t_txt for k in keywords):
                                        found = True
                                        target_name = t_txt
                                        break
                        except: continue

                    if found:
                        print(f"!!! ターゲット捕捉: '{target_name}' !!!")
                        print("F12 プロトコルを自動発動します。")
                        
                        # 師匠のホットキーを発動
                        keyboard.press_and_release('f12')
                        
                        # 連射を避けるための待機 (2秒)
                        time.sleep(2.0)
                        break
            except: pass
            
            # 高速監視
            time.sleep(0.1)
            
    except Exception as e:
        pass

if __name__ == "__main__":
    sentinel_observer_v69()
 Greenland
