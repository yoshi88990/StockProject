import ctypes
import win32api
import time
import os

def eye_log():
    log_file = r"C:\StockProject\eye_color_diag.txt"
    try:
        while True:
            cur_pos = win32api.GetCursorPos()
            hdc = ctypes.windll.user32.GetDC(0)
            pixel = ctypes.windll.gdi32.GetPixel(hdc, cur_pos[0], cur_pos[1])
            r, g, b = pixel & 0xFF, (pixel >> 8) & 0xFF, (pixel >> 16) & 0xFF
            ctypes.windll.user32.ReleaseDC(0, hdc)
            
            with open(log_file, "w") as f:
                f.write(f"POS:({cur_pos[0]},{cur_pos[1]}) RGB:({r},{g},{b}) Time:{time.strftime('%H:%M:%S')}")
            
            time.sleep(0.5)
            # ESC で停止
            if win32api.GetAsyncKeyState(0x1B) & 0x8000: break
    except Exception as e:
        with open(log_file, "a") as f: f.write(f"\nError: {e}")

if __name__ == "__main__":
    eye_log()
