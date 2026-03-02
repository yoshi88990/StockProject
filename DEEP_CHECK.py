import pywinauto
import sys

sys.stdout.reconfigure(encoding='utf-8')

def deep_visual_check():
    print("【深層部UIスキャン報告】")
    try:
        desktop = pywinauto.Desktop(backend="uia")
        found = False
        for win in desktop.windows():
            title = win.window_text()
            # 「Run command?」が含まれるウィンドウを探す
            if "Run" in title or not title:
                btns = win.descendants(control_type="Button")
                for btn in btns:
                    name = btn.window_text()
                    if name:
                        rect = btn.rectangle()
                        print(f"・ボタン発見: '{name}' | ウィンドウ: '{title}'")
                        print(f"  - 座標: ({rect.left}, {rect.top}) - ({rect.right}, {rect.bottom})")
                        found = True
        if not found:
            print("・ボタンは検出されませんでした。")
    except Exception as e:
        print(f"・エラー: {e}")

if __name__ == "__main__":
    deep_visual_check()
