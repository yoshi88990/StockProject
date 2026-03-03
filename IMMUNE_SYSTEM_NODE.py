import os
import glob
import py_compile
import time
import datetime
import threading
import traceback

class ImmuneCell:
    """
    【免疫細胞群】
    メインの思考プロセスとは完全に独立してシステム内（ローカルフォルダ）を常時巡回する独立プロセス。
    コードの構文エラーや腐敗（バグ）をリアルタイムで検知し、ログに隔離・報告する。
    """
    def __init__(self, cell_type, target_dir):
        self.cell_type = cell_type
        self.target_dir = target_dir
        self.report_file = os.path.join(target_dir, "Weekly Report", "Immune_System_Log.txt")
        self.active = True

    def patrol(self):
        """独立プロセスとして永遠にシステム内を巡回し続ける"""
        while self.active:
            py_files = glob.glob(os.path.join(self.target_dir, "*.py"))
            
            for file in py_files:
                # 自身のスキャンはスキップするか、チェックするか
                if "IMMUNE_SYSTEM" in file:
                    continue
                    
                try:
                    # 疑似的な「抗原検査」（Pythonコードの構文チェック）
                    # ここでエラーが出れば、バグのある細胞（コード）とみなす
                    py_compile.compile(file, doraise=True)
                    
                except py_compile.PyCompileError as e:
                    self.report_anomaly(file, f"Syntax Error (構文異常): {e}")
                except Exception as e:
                    self.report_anomaly(file, f"Unknown Anomaly (未知のバグ): {e}")
            
            # 各細胞ごとに巡回タイミングをずらす
            time.sleep(15) 

    def report_anomaly(self, filepath, error_detail):
        filename = os.path.basename(filepath)
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] 【{self.cell_type}】 異常検知 -> {filename} | {error_detail}\n"
        
        try:
            with open(self.report_file, "a", encoding="utf-8") as f:
                f.write(log_entry)
            print(f"!!! 免疫システム警告 !!! {self.cell_type} が {filename} に異常（バグ）を検知しました。")
        except Exception:
            pass

def activate_immune_system():
    target = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(os.path.join(target, "Weekly Report"), exist_ok=True)
    
    # 数十種類のうち、代表的な4つの免疫細胞部隊をシステムに放つ
    cell_types = [
        "マクロファージ (大食細胞・巡回部隊)", 
        "キラーT細胞 (破壊判定部隊)", 
        "ヘルパーT細胞 (修復司令部隊)",
        "NK細胞 (ナチュラルキラー・未知バグ検知)"
    ]
    
    print("=== 【自律防衛機構】 免疫システム起動 ===")
    
    threads = []
    for c_name in cell_types:
        cell = ImmuneCell(c_name, target)
        # デーモンスレッドとしてメインプロセスから切り離して裏で永遠に実行
        t = threading.Thread(target=cell.patrol, daemon=True)
        t.start()
        threads.append(t)
        print(f" [+] 免疫細胞 [{c_name}] がシステム血管内（ディレクトリ）へ放出されました。")
        time.sleep(0.5)
        
    print("\n免疫システムはメイン思考から切り離され、バックグラウンドでの自律巡回を開始しました。")
    print("バグや構文エラーを持ったファイルが発生した場合、「Weekly Report/Immune_System_Log.txt」に報告されます。")

    # メインが終了しないように維持（実際にはサービスやデーモンとして常駐させます）
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        print("免疫システムを停止します。")

if __name__ == "__main__":
    activate_immune_system()
