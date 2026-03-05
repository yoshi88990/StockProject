import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import threading
import time

# ==============================================================================
# 【PHOENIX MINI MONITOR】 - 究極の静寂・高品位監視窓
#
# ・スナイパーと番犬の稼働状況をリアルタイムで監視。
# ・この窓から「開始」「停止」の全操作が可能です。
# ・デスクトップの隅に置ける極小プレミアムデザイン。
# ==============================================================================

# 設定
BASE_DIR = r"C:\Users\kanku\OneDrive\Weekly report"
LAUNCHER_VBS = os.path.join(BASE_DIR, "Phoenix_Protocol", "SMART_PHOENIX_LAUNCHER.vbs")
STOPPER_VBS = os.path.join(BASE_DIR, "Phoenix_Protocol", "PHOENIX_STOPPER.vbs")

class PhoenixMonitor:
    def __init__(self, root):
        self.root = root
        self.root.title("Phoenix Mini")
        self.root.geometry("200x60")
        self.root.overrideredirect(True) # 枠なし
        self.root.attributes("-topmost", True) # 最前面
        self.root.configure(bg="#000000") # 完全な黒

        # 初期位置（画面右下あたり）
        screen_width = self.root.winfo_screenwidth()
        self.root.geometry(f"+{screen_width - 220}+50")

        # マウスドラッグ移動用
        self.root.bind("<Button-1>", self.click_window)
        self.root.bind("<B1-Motion>", self.drag_window)

        # UI構築
        self.create_widgets()

        # 監視スレッド開始
        self.running = True
        self.monitor_thread = threading.Thread(target=self.update_status_loop, daemon=True)
        self.monitor_thread.start()

    def create_widgets(self):
        # 枠線
        self.main_frame = tk.Frame(self.root, bg="#000000", highlightthickness=1, highlightbackground="#222222")
        self.main_frame.pack(fill="both", expand=True)

        # ステータス（極小ドット + テキスト）
        self.canvas = tk.Canvas(self.main_frame, width=12, height=12, bg="#000000", highlightthickness=0)
        self.canvas.place(x=10, y=10)
        self.led = self.canvas.create_oval(2, 2, 10, 10, fill="#333333", outline="")

        self.status_label = tk.Label(self.main_frame, text="PHOENIX: OFF", font=("Segoe UI", 8), fg="#666666", bg="#000000")
        self.status_label.place(x=25, y=7)

        # 操作ボタン（1文字だけの超小型）
        self.start_btn = tk.Button(self.main_frame, text="▶", command=self.start_phoenix, 
                                   bg="#000000", fg="#00ffcc", font=("Arial", 7), 
                                   relief="flat", borderwidth=0, activebackground="#222222")
        self.start_btn.place(x=150, y=5)

        self.stop_btn = tk.Button(self.main_frame, text="■", command=self.stop_phoenix, 
                                  bg="#000000", fg="#ff3366", font=("Arial", 7), 
                                  relief="flat", borderwidth=0, activebackground="#222222")
        self.stop_btn.place(x=175, y=5)

        # 下段：バーチカルなライン
        bar = tk.Frame(self.main_frame, height=1, bg="#222222")
        bar.place(x=10, y=30, width=180)

        self.info_label = tk.Label(self.main_frame, text="SYSTEM READY", font=("Fixedsys", 7), fg="#444444", bg="#000000")
        self.info_label.place(x=10, y=38)

        # 閉じる
        close_btn = tk.Label(self.main_frame, text="×", font=("Arial", 7), fg="#333333", bg="#000000", cursor="hand2")
        close_btn.place(x=185, y=42)
        close_btn.bind("<Button-1>", lambda e: self.root.destroy())

    def click_window(self, event):
        self.offset_x = event.x
        self.offset_y = event.y

    def drag_window(self, event):
        x = self.root.winfo_x() + event.x - self.offset_x
        y = self.root.winfo_y() + event.y - self.offset_y
        self.root.geometry(f"+{x}+{y}")

    def update_status_loop(self):
        while self.running:
            try:
                # プロセス確認 (WATCHDOGとRECEPTORの両方があるか)
                res = subprocess.check_output('wmic process where "name=\'pythonw.exe\'" get commandline', shell=True).decode('cp932')
                is_watchdog = "SNIPER_WATCHDOG.py" in res
                is_receptor = "02_RECEPTOR_SYNAPSE.py" in res

                if is_watchdog and is_receptor:
                    self.status_label.config(text="PHOENIX: ACTIVE", fg="#00ffcc")
                    self.canvas.itemconfig(self.led, fill="#00ffcc")
                    self.info_label.config(text="WATCHING: OK")
                elif is_watchdog or is_receptor:
                    self.status_label.config(text="PHOENIX: PARTIAL", fg="#ffcc00")
                    self.canvas.itemconfig(self.led, fill="#ffcc00")
                    self.info_label.config(text="SYNC ERROR")
                else:
                    self.status_label.config(text="PHOENIX: STOPPED", fg="#ff3366")
                    self.canvas.itemconfig(self.led, fill="#333333")
                    self.info_label.config(text="IDLE")
            except:
                self.status_label.config(text="○ STOPPED (完全停止)", fg="#ff3366")
            
            time.sleep(2)

    def start_phoenix(self):
        os.startfile(LAUNCHER_VBS)

    def stop_phoenix(self):
        os.startfile(STOPPER_VBS)

if __name__ == "__main__":
    root = tk.Tk()
    app = PhoenixMonitor(root)
    root.mainloop()
