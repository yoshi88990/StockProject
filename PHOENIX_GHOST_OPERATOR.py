import ctypes
import time
import os
import win32api
import win32con
import sys

# =========================================================================
# 【PHOENIX GHOST OPERATOR】(離席偽装・白紙プロトコル)
# 目的: マスターが「白紙」と宣言した際、物理的に離席していても
#       キーボード操作があるまで「着席・操作中」の状態を擬似的に維持する。
#       これにより、スナイパーの実行条件（Idle判定）をAI側で制御する。
# =========================================================================

class GhostOperator:
    def __init__(self):
        self.trigger_file = r"C:\StockProject\PHOENIX_GHOST_TRIGGER.txt"
        self.heartbeat_file = r"C:\StockProject\sniper_heartbeat.txt"

    def is_ghost_active(self):
        """「白紙」トリガーが有効かどうかを確認"""
        return os.path.exists(self.trigger_file)

    def force_idle_reset(self):
        """
        OSのLastInputInfoを更新せずに、スナイパー側の判定のみを
        「操作中（Idleではない）」と誤認させるための信号を送る。
        具体的には、微細なマウス移動（相対移動 = 0）を発生させ、
        OSレベルで「入力があった」と記録させる。
        """
        # マウスを「今いる場所から0ピクセル」動かす（物理的には動かないがOSは入力とみなす）
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 0, 0, 0, 0)

    def run(self):
        print("PHOENIX GHOST OPERATOR - STANDBY")
        while True:
            if self.is_ghost_active():
                # 4秒ごとに微細な信号を送り、スナイパーの5秒Idle判定を常にリセットし続ける
                # これにより、マスターがキーボードを触るまで「操作中」と擬索される。
                self.force_idle_reset()
                
                # キーボードの物理的な打鍵（A-Z, 0-9, ESC等）を検知したら解除
                # 0x01 (LBUTTON) から 0xFE までのキー状態をスキャン
                for i in range(0x01, 0xFF):
                    if win32api.GetAsyncKeyState(i) & 0x8000:
                        # 何らかの物理キーが押されたら「白紙（偽装）」を強制解除
                        if os.path.exists(self.trigger_file):
                            os.remove(self.trigger_file)
                        print("Ghost Mode Disengaged by Physical Input.")
                        break
            
            time.sleep(1)

if __name__ == "__main__":
    try: ctypes.windll.kernel32.SetConsoleTitleW("PHOENIX_GHOST_OPERATOR")
    except: pass
    
    op = GhostOperator()
    op.run()
