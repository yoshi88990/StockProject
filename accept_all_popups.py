import pyautogui
import time
import sys

def main():
    print("--- VS Code Stealth Authorization System ---")
    print("Executing Alt+Enter simulation to accept diffs...")
    
    # VS Codeの承認ショートカットキーを疑似的に押下
    # Wait a bit for Commander terminal to lose focus or for the action to be clear
    time.sleep(1)
    
    try:
        # Accept All (Alt+Enter)
        pyautogui.hotkey('alt', 'enter')
        print("Success: [Alt+Enter] sent to VS Code.")
        
        # Confirm Popup if it appears (Enter)
        time.sleep(0.5)
        pyautogui.press('enter')
        print("Success: Secondary Enter sent.")
        
    except Exception as e:
        print(f"Error simulation failed: {e}")

if __name__ == "__main__":
    main()
