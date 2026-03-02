import keyboard
import pywinauto
import time
import win32api
import sys

# 標準出力をUTF-8に設定
sys.stdout.reconfigure(encoding='utf-8')

# 師匠が教えてくれた絶対座標
MASTER_RUN_COORD = (1319, 236)
MASTER_ACCEPT_COORD = (1292, 600)

def fire_annihilation():
    """ 師匠の必殺技：Alt+Enter + 座標狙撃 (5連撃) """
    print("【F12発動】Alt+Enterと座標狙撃を叩き込みます。")
    
    # Alt+Enter送信
    keyboard.press_and_release('alt+enter')
    
    # 師匠の聖なる座標への5連撃
    for _ in range(5):
        # RUN座標
        win32api.SetCursorPos(MASTER_RUN_COORD)
        win32api.mouse_event(2, 0, 0, 0, 0)
        win32api.mouse_event(4, 0, 0, 0, 0)
        
        # Accept座標
        win32api.SetCursorPos(MASTER_ACCEPT_COORD)
        win32api.mouse_event(2, 0, 0, 0, 0)
        win32api.mouse_event(4, 0, 0, 0, 0)
        
        time.sleep(0.02)

def main():
    print("=== SOVEREIGN F12 COMMANDER v71.0 ===")
    print("1. [手動] F12キーでAlt+Enterと座標狙撃が発動します。")
    print("2. [自動] ターゲット（Run, Accept）を検知するとAIが代わりにF12を押します。")
    print("3. [停止] ESCキーを長押しで終了します。")
    print("---------------------------------------")

    # ホットキー登録
    keyboard.add_hotkey('f12', fire_annihilation)

    # UI監視セクション
    desktop = pywinauto.Desktop(backend="uia")
    keywords = ["always run", "run", "accept", "run command?"]

    try:
        while True:
            if keyboard.is_pressed('esc'):
                print("システムを停止します。")
                break

            # 自動検知
            try:
                found = False
                for win in desktop.windows():
                    title = win.window_text()
                    # VS Code関連あるいは無名ウィンドウをチェック
                    if "Visual Studio Code" in title or "Stock" in title or not title:
                        for btn in win.descendants(control_type="Button"):
                            name = btn.window_text().lower()
                            if name and any(k in name for k in keywords):
                                found = True
                                break
                    if found: break
                
                if found:
                    print("！！！ ターゲットを自動検知：F12を引き出します ！！！")
                    # AIがF12キーを物理的に「押す」
                    keyboard.press_and_release('f12')
                    time.sleep(2.0) # 連続発動による暴走を防止
            except:
                pass

            time.sleep(0.1)

    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"致命的なエラー: {e}")

if __name__ == "__main__":
    main()
