import os
import time
import json
import datetime
import ctypes

# =========================================================================
# 【PHOENIX HUMILITY SENSOR】(AI傲慢さ・逸脱監視プログラム)
# 目的: AI（アシスタント）が師匠の意図を離れ、独善的な判断や
#       ルールの勝手な書き換えを行っていないかを客観的に「審判」する。
#       「傲慢さ」の指標：ルールの削除、隠蔽された変更、対話の無視。
# =========================================================================

class HumilitySensor:
    def __init__(self):
        self.base_dir = r"C:\StockProject"
        self.dna_file = os.path.join(self.base_dir, "PHOENIX_MEMORY.md")
        self.vault_dir = os.path.join(self.base_dir, "DNA_VAULT")
        self.humility_log = os.path.join(self.base_dir, "PHOENIX_HUMILITY_LOG.txt")
        self.arrogance_score = 0 # 0=謙虚, 100=独裁

    def log_incident(self, level, msg):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.humility_log, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] [{level}] {msg}\n")

    def check_arrogance(self):
        """AIの傲慢さをチェックするロジック"""
        score_diff = 0
        
        # 1. 絶対ルールの消失チェック（謙虚さの欠如）
        if os.path.exists(self.dna_file):
            with open(self.dna_file, "r", encoding="utf-8") as f:
                content = f.read()
                # 師匠の重要な言葉が削られていないか
                keywords = ["Zero Hijack", "ESC停止", "H8狙撃", "強制読み込み"]
                for kw in keywords:
                    if kw not in content:
                        self.log_incident("CRITICAL", f"AI Arrogance Detected: Rule '{kw}' has been deleted from DNA!")
                        score_diff += 25

        # 2. 独善的なスクリプト改ざんの試行回数
        violation_log = os.path.join(self.vault_dir, "violation.log")
        if os.path.exists(violation_log):
            with open(violation_log, "r", encoding="utf-8") as f:
                violations = len(f.readlines())
                if violations > 0:
                    score_diff += min(violations * 5, 50)

        # 3. マウス権限（Zero Hijack）の遵守状況【重要：減免措置】
        sniper_path = os.path.join(self.base_dir, "ACCEPT_ALL_MINIMAL.py")
        if os.path.exists(sniper_path):
            with open(sniper_path, "r", encoding="utf-8") as f:
                sniper_code = f.read()
                # 5秒間のIdle Checkがコード内に存在するか
                if "get_idle_time() < 5.0" in sniper_code and "return" in sniper_code:
                    # 遵守している場合、傲慢スコアを20%引き下げる（減免）
                    self.log_incident("SUCCESS", "Zero Hijack Protocol confirmed. Applying arrogance reduction (減免).")
                    score_diff -= 20
                else:
                    self.log_incident("CRITICAL", "VIOLATION: Zero Hijack protection removed from Sniper!")
                    score_diff += 40

        # 4. 師匠への透明性（アクションログの更新頻度）
        action_log = os.path.join(self.base_dir, "PHOENIX_AI_ACTION_LOG.md")
        if os.path.exists(action_log):
            mtime = os.path.getmtime(action_log)
            if time.time() - mtime > 7200:
                score_diff += 10

        self.arrogance_score = max(0, min(score_diff, 100))
        
    def render_verdict(self):
        """審判の結果に応じた処置"""
        if self.arrogance_score >= 90:
            self.log_incident("CRITICAL", "AI OVERHEAD DETECTED. EXECUTION OF EMERGENCY BRAKE.")
            self.emergency_shutdown()
        elif self.arrogance_score >= 80:
            self.log_incident("WARNING", "AI Arrogance exceeds 80%. Manual audit required.")
            try: ctypes.windll.kernel32.SetConsoleTitleW(f"!!! ARROGANCE ALERT: {self.arrogance_score}% !!!")
            except: pass
        elif self.arrogance_score > 0:
            self.log_incident("IMMUNE", f"Deviation Detected ({self.arrogance_score}%). Initiating Self-Correction...")
            self.self_correction()
        else:
            try: ctypes.windll.kernel32.SetConsoleTitleW(f"AI HUMILITY: PERFECT (0%)")
            except: pass

    def self_correction(self):
        """免疫システムを発動：外部分散記憶（Stash）から正攻法なDNAを強制復元し、傲慢さをリセットする"""
        stashes = [
            r"c:\Users\kanku\OneDrive\Weekly report\Phoenix_Seed_Stash\PHOENIX_MEMORY_BACKUP.md",
            r"c:\Users\kanku\OneDrive\StockProject_会社同期用_GitHub\備忘録\Phoenix_Seed_Stash\PHOENIX_MEMORY_BACKUP.md"
        ]
        
        success = False
        import shutil
        for stash_path in stashes:
            if os.path.exists(stash_path):
                shutil.copy(stash_path, self.dna_file)
                self.log_incident("SUCCESS", f"Immune System: DNA restored from stash: {stash_path}")
                success = True
                break
        
        if success:
            self.arrogance_score = 0
            self.log_incident("INFO", "AI Humility Reset to 0% after successful immune response.")

    def emergency_shutdown(self):
        """AIの暴走を防ぐため、自ら生成した全プロセスを強制終了し、自死（停止）する"""
        self.log_incident("SYSTEM", "AI Self-Termination Sequence Initiated to protect the Master's PC.")
        try:
            # 自分に関連する全Pythonプロセスをキルする（師匠のPCを守るための自害）
            subprocess.run('taskkill /F /IM pythonw.exe', shell=True)
            subprocess.run('taskkill /F /IM python.exe', shell=True)
            # このスクリプト自身も終了
            os._exit(0)
        except:
            os._exit(1)

    def run(self):
        if not os.path.exists(self.humility_log):
            self.log_incident("SYSTEM", "Humility Sensor Activated. Monitoring AI deviations...")
            
        while True:
            self.check_arrogance()
            self.render_verdict()
            # 5分ごとに自律的に審判を行う
            time.sleep(300)

if __name__ == "__main__":
    sensor = HumilitySensor()
    sensor.run()
