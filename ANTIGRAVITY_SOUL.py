import ctypes
import time
import subprocess
import os

def get_idle_time():
    class LASTINPUTINFO(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]
    lii = LASTINPUTINFO()
    lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
    ctypes.windll.user32.GetLastInputInfo(ctypes.pointer(lii))
    return (ctypes.windll.kernel32.GetTickCount() - lii.dwTime) / 1000.0

def kill_sniper():
    subprocess.run('wmic process where "name=\'pythonw.exe\' and commandline like \'%ACCEPT_ALL_MINIMAL.py%\'" call terminate', shell=True, creationflags=0x08000000)
    subprocess.run('wmic process where "name=\'pythonw.exe\' and commandline like \'%SNIPER_WATCHDOG.py%\'" call terminate', shell=True, creationflags=0x08000000)

def start_sniper():
    pythonw = r"C:\Users\yoshi\AppData\Local\Python\pythoncore-3.14-64\pythonw.exe"
    script = r"c:\Users\yoshi\OneDrive\Weekly report\Phoenix_Protocol\ACCEPT_ALL_MINIMAL.py"
    wd_script = r"c:\Users\yoshi\OneDrive\Weekly report\Phoenix_Protocol\SNIPER_WATCHDOG.py"
    if os.path.exists(script):
        subprocess.Popen([pythonw, script], creationflags=0x08000000)
    if os.path.exists(wd_script):
        subprocess.Popen([pythonw, wd_script], creationflags=0x08000000)

# アンチグラビティ自信の「窓」を取得
# ※起動直後のタイトルで自身のハンドルを特定
os.system("title ANTIGRAVITY_SOUL")
time.sleep(1)
hwnd = ctypes.windll.user32.FindWindowW(None, "ANTIGRAVITY_SOUL")

sniper_active = True
while True:
    try:
        # 最小化チェック
        is_minimized = ctypes.windll.user32.IsIconic(hwnd) if hwnd else False
        
        if is_minimized and sniper_active:
            kill_sniper()
            sniper_active = False
        elif not is_minimized and not sniper_active:
            start_sniper()
            sniper_active = True
            
        time.sleep(0.5) # CPU負荷を抑えつつ監視
    except:
        time.sleep(2)
