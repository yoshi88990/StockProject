import os
import shutil
import datetime

# 師匠のWindows環境における「マイドキュメント」フォルダの一般的なパスを取得
# （OneDrive経由でマイドキュメントが同期されている場合も考慮）
base_docs = os.path.join(os.environ['USERPROFILE'], 'Documents')
if not os.path.exists(base_docs):
    base_docs = os.path.join(os.environ['USERPROFILE'], 'OneDrive', 'ドキュメント')
    if not os.path.exists(base_docs):
        # 最終フォールバック
        base_docs = os.environ['USERPROFILE']

BACKUP_DIR = os.path.join(base_docs, 'StockProject_Redundant_Backup')

def create_local_snapshot(source_dir):
    """
    指定されたプロジェクトフォルダ全体をZIP化し、安全な別領域へバックアップする。
    """
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
        
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_filename = f"StockProject_Snapshot_{timestamp}"
    backup_path = os.path.join(BACKUP_DIR, backup_filename)
    
    try:
        # フォルダ全体をZIP圧縮
        shutil.make_archive(backup_path, 'zip', source_dir)
        print(f"【冗長化成功】ローカルスナップショットの作成完了: {backup_path}.zip")
        return True
    except Exception as e:
        print(f"【警告】バックアップの作成中にエラーが発生しました: {e}")
        return False

if __name__ == "__main__":
    # 現在のスクリプトの親ディレクトリ（StockProjectフォルダ）を対象とする
    target_project = os.path.dirname(os.path.abspath(__file__))
    create_local_snapshot(target_project)
