import win32api
import win32con
import time
import sys

# Ensure stdout uses a safe encoding to prevent cp932 errors
sys.stdout.reconfigure(encoding='utf-8')

print("【Start Test】5 seconds later, sending Alt+Enter...")
print("Please leave the 'Run Alt+Enter' waiting screen open and do not touch for 5 seconds!")

time.sleep(5)

VK_MENU = 0x12  # Alt
VK_RETURN = 0x0D # Enter

print(">>> Firing Snipe! (Alt + Enter) <<<")
# Press Alt
win32api.keybd_event(VK_MENU, 0, 0, 0)
time.sleep(0.01)
# Press Enter
win32api.keybd_event(VK_RETURN, 0, 0, 0)
time.sleep(0.05)
# Release Enter
win32api.keybd_event(VK_RETURN, 0, win32con.KEYEVENTF_KEYUP, 0)
# Release Alt
win32api.keybd_event(VK_MENU, 0, win32con.KEYEVENTF_KEYUP, 0)

print("Test finished. Did the button react?")
