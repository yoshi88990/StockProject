import ctypes
import time
import subprocess
import os

os.system("title ANTIGRAVITY_CONFIDENCE")
time.sleep(1)
hwnd = ctypes.windll.user32.FindWindowW(None, "ANTIGRAVITY_CONFIDENCE")

def manage_sniper(action):
    # スナイパーと番犬を葬る／復活させる
    if action == "kill":
        subprocess.run('wmic process where \"name=\'pythonw.exe\' and commandline like \'%ACCEPT_ALL_MINIMAL.py%\'\" call terminate', shell=True, creationflags=0x08000000)
        subprocess.run('wmic process where \"name=\'pythonw.exe\' and commandline like \'%SNIPER_WATCHDOG.py%\'\" call terminate', shell=True, creationflags=0x08000000)
    elif action == "start":
        pw = r"C:\Users\yoshi\AppData\Local\Python\pythoncore-3.14-64\pythonw.exe"
        sc = r"c:\Users\yoshi\OneDrive\Weekly report\Phoenix_Protocol\ACCEPT_ALL_MINIMAL.py"
        wd = r"c:\Users\yoshi\OneDrive\Weekly report\Phoenix_Protocol\SNIPER_WATCHDOG.py"
        subprocess.Popen([pw, sc], creationflags=0x08000000)
        subprocess.Popen([pw, wd], creationflags=0x08000000)

sniper_active = True
manage_sniper("start") # 初期起動

while True:
    try:
        is_min = ctypes.windll.user32.IsIconic(hwnd) if hwnd else False
        if is_min and sniper_active:
            manage_sniper("kill")
            sniper_active = False
        elif not is_min and not sniper_active:
            manage_sniper("start")
            sniper_active = True
        time.sleep(0.5)
    except: time.sleep(2)
