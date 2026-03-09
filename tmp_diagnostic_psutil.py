import psutil
import time
import os

PROCS_TO_WATCH = {
    "Sniper (DNA_SNIPER)": "DNA_SNIPER_APP.py",
    "機械打ち (Mechanical)": "ACCEPT_ALL_MINIMAL.py",
    "司令 (Commander)": "commander.py",
    "誠実監視 (Sincerity)": "PHOENIX_HUMILITY_SENSOR.py",
    "受容接続 (Receptor)": "PHOENIX_DNA_SYNCHRONIZER.py",
    "四半期監視 (Sentinel)": "PHOENIX_SENTINEL.py",
    "知能計算 (Calculator)": "PHOENIX_INTEL_CALCULATOR.py",
    "深層解析 (Analyst)": "PHOENIX_ANALYST_CORE.py"
}

def check_process_alive(script_name):
    t0 = time.time()
    found = False
    for proc in psutil.process_iter(['cmdline']):
        try:
            cmd = proc.info.get('cmdline')
            if cmd and any(script_name.lower() in arg.lower() for arg in cmd):
                found = True
                break
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    t1 = time.time()
    print(f"Checked {script_name}: {found} (Took {t1-t0:.4f}s)")
    return found

if __name__ == "__main__":
    t_start = time.time()
    for name, script in PROCS_TO_WATCH.items():
        check_process_alive(script)
    t_end = time.time()
    print(f"Total time: {t_end-t_start:.4f}s")
