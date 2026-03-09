import win32gui
import win32api
import ctypes
import os
import time

def diag_colors():
    q = chr(34)
    log_path = r"C:\StockProject\sniper_diag.txt"
    
    try:
        hwnd = win32gui.GetForegroundWindow()
        title = win32gui.GetWindowText(hwnd)
        rect = win32gui.GetWindowRect(hwnd)
        w_l, w_t, w_r, w_b = rect
        
        scan_left = max(w_l, w_r - 500)
        
        hdc = ctypes.windll.user32.GetDC(0)
        matches = []
        
        # 10px間隔で色をサンプリング
        for ty in range(w_t, w_b, 10):
            for tx in range(scan_left, w_r, 10):
                pixel = ctypes.windll.gdi32.GetPixel(hdc, tx, ty)
                r, g, b = pixel & 0xFF, (pixel >> 8) & 0xFF, (pixel >> 16) & 0xFF
                
                # 青っぽい色を全部出す
                if b > 70 and b > r:
                    matches.append(f"Pos:({tx},{ty}) RGB:({r},{g},{b})")
        
        ctypes.windll.user32.ReleaseDC(0, hdc)
        
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(f"Active Window: {title}\n")
            f.write(f"Window Rect: {rect}\n")
            f.write(f"Detected potential blues: {len(matches)}\n")
            f.write("\n".join(matches[:50]))
            
    except Exception as e:
        with open(log_path, "w", encoding="utf-8") as f:
            f.write(f"Error: {str(e)}")

if __name__ == "__main__":
    diag_colors()
