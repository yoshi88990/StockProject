import pywinauto
import sys

sys.stdout.reconfigure(encoding='utf-8')

def find_run_command_dialog():
    print("【Run command? ダイアログ追跡】")
    try:
        desktop = pywinauto.Desktop(backend="uia")
        for win in desktop.windows():
            # ウィンドウタイトルがない場合が多いので、子要素を走査
            try:
                # 「Run command?」というテキストを持つ要素を探す
                # または、class_name が Chrome_WidgetWin_1 (VS Code のポップアップ可能性)
                children = win.descendants()
                for child in children:
                    txt = child.window_text()
                    if "Run command?" in txt:
                        rect = child.rectangle()
                        print(f"!!! 発見 !!!: 'Run command?' テキスト | ウィンドウ: '{win.window_text()}'")
                        print(f"位置: {rect}")
                        
                        # そのウィンドウ内の「Button」をすべて列挙
                        btns = win.descendants(control_type="Button")
                        for btn in btns:
                            b_txt = btn.window_text()
                            b_rect = btn.rectangle()
                            print(f"  ・ボタン: '{b_txt}' at {b_rect}")
            except:
                continue
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    find_run_command_dialog()
