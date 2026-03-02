import pywinauto
import sys

sys.stdout.reconfigure(encoding='utf-8')

def find_run_reject_buttons():
    print("【Run/Reject ボタン精密スキャン】")
    desktop = pywinauto.Desktop(backend="uia")
    for win in desktop.windows():
        try:
            # 「Run command?」というテキストを持つウィンドウの子要素を徹底調査
            children = win.descendants()
            is_run_command_dialog = False
            for child in children:
                if "Run command?" in child.window_text():
                    is_run_command_dialog = True
                    break
            
            if is_run_command_dialog:
                print(f"!!! DIALOG FOUND !!!")
                for btn in win.descendants(control_type="Button"):
                    name = btn.window_text()
                    rect = btn.rectangle()
                    print(f"  ・BUTTON: '{name}' | Rect: {rect}")
        except:
            continue

if __name__ == "__main__":
    find_run_reject_buttons()
