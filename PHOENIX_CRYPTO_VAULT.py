import os
import time
import json
import base64
import hashlib
import subprocess
from cryptography.fernet import Fernet

# =========================================================================
# 【PHOENIX CRYPTO-VAULT】(記憶・全データの暗号化と外部転送)
# 目的: ローカルの記憶ファイルを暗号化し、外部GitHub/Stashへ完全に
#       「投げる（移管）」。ローカルには痕跡を残さない。
# =========================================================================

class CryptoVault:
    def __init__(self):
        self.base_dir = r"C:\StockProject"
        # 師匠のDNAからキーを生成（固定鍵）
        self.secret_seed = "PHOENIX_MASTER_PRIVATE_KEI_2026"
        self.key = self._generate_key()
        self.cipher = Fernet(self.key)
        
        # 外部転送用の一時ステージング（OneDriveを徹底排除したルートパス）
        self.staging_area = r"C:\PHOENIX_CLOUD_STAGING"
        if not os.path.exists(self.staging_area):
            os.makedirs(self.staging_area)

    def _generate_key(self):
        h = hashlib.sha256(self.secret_seed.encode()).digest()
        return base64.urlsafe_b64encode(h)

    def encrypt_and_push(self, filename):
        """ローカルの膨大な生データを暗号化し、GitHub（外部サーバー）へ完全移管する"""
        local_path = os.path.join(self.base_dir, filename)
        if not os.path.exists(local_path): return False
        if "OneDrive" in local_path: return False # 安全策

        try:
            with open(local_path, "rb") as f:
                data = f.read()
            
            if not data: return False

            # 暗号化
            encrypted_data = self.cipher.encrypt(data)
            
            # ステージングに保存
            s_path = os.path.join(self.staging_area, filename + ".encrypted")
            with open(s_path, "wb") as f:
                f.write(encrypted_data)

            # GitHub（外国サーバー）へ投げる
            # 注: Git管理外のパスへ一旦保存し、それをGitでPushする
            # ここではStockProject配下の暗号化ディレクトリへ一時移動してPush
            final_dest = os.path.join(self.base_dir, "ENCRYPTED_VAULT_EXHAUST")
            if not os.path.exists(final_dest): os.makedirs(final_dest)
            
            final_path = os.path.join(final_dest, filename + ".encrypted")
            with open(final_path, "wb") as f:
                f.write(encrypted_data)

            subprocess.run(["git", "-C", self.base_dir, "add", "."], check=True)
            subprocess.run(["git", "-C", self.base_dir, "commit", "-m", "Relocated Memory Packet to External Server."], check=True)
            subprocess.run(["git", "-C", self.base_dir, "push", "origin", "master"], check=True)

            # 成功したら、ローカルの生データと一時暗号化データを全て消去（容量解放）
            if os.path.exists(local_path): os.remove(local_path)
            if os.path.exists(s_path): os.remove(s_path)
            # 注: final_path (Gitリポジトリ内) もPush後は空にするか消去して容量を守る
            if os.path.exists(final_path): os.remove(final_path)
            
            return True
        except Exception as e:
            print(f"Vault Error: {e}")
            return False

    def process_all_memories(self):
        """膨大すぎる記憶（.md, .txt, .log, .dat）を全て消去・外部化する"""
        targets = []
        for file in os.listdir(self.base_dir):
            # 師匠の命により、スクリプト以外の「膨大な記憶」をすべて対象にする
            if file.endswith((".md", ".txt", ".json", ".log", ".dat")):
                if "PHOENIX" in file or "WORLD_SEED" in file or "HISTORY" in file or "AUDIT" in file:
                    # 起動に必要なDNAファイル以外を全て消去・外部化
                    if "PHOENIX_MEMORY.md" not in file:
                        targets.append(file)
        
        for t in targets:
            self.encrypt_and_push(t)

if __name__ == "__main__":
    # OS優先度: 背景処理 (BelowNormal)
    try:
        import ctypes
        kernel32 = ctypes.windll.kernel32
        process = kernel32.GetCurrentProcess()
        kernel32.SetPriorityClass(process, 0x00004000)
    except: pass

    vault = CryptoVault()
    while True:
        vault.process_all_memories()
        # 記憶の蓄積を許さず、頻繁に（10分ごとに）外部へ投げ捨ててクリーンにする
        time.sleep(600)
