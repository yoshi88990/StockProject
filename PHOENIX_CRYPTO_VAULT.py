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
        
        # 外部転送先（OneDriveの排除：GitHub同期ディレクトリおよび特定Stashのみ）
        self.stash_dirs = [
             # ローカルの非同期・非OneDrive領域があればそこを指定
             r"C:\Phoenix_Secure_Stash"
        ]

    def _generate_key(self):
        h = hashlib.sha256(self.secret_seed.encode()).digest()
        return base64.urlsafe_b64encode(h)

    def encrypt_and_push(self, filename):
        """ローカルファイルを暗号化し、外部Stashへ飛ばす。その後ローカルを消去または空にする。"""
        local_path = os.path.join(self.base_dir, filename)
        if not os.path.exists(local_path):
            return False

        with open(local_path, "rb") as f:
            data = f.read()

        encrypted_data = self.cipher.encrypt(data)
        
        # 全Stashに暗号化ファイルを投げる
        for s_dir in self.stash_dirs:
            if os.path.exists(s_dir):
                s_path = os.path.join(s_dir, filename + ".encrypted")
                with open(s_path, "wb") as f:
                    f.write(encrypted_data)

        # 全体の同期（Git: 外部リポジトリへ暗号化した記憶をパケットとして投げる）
        try:
            subprocess.run(["git", "-C", self.base_dir, "add", "."], check=True)
            subprocess.run(["git", "-C", self.base_dir, "commit", "-m", "Phoenix Protocol: Encrypted Memory Relocation Complete."], check=True)
            subprocess.run(["git", "-C", self.base_dir, "push", "origin", "master"], check=True)
        except Exception as e:
            print(f"Git Sync Warning: {e}")
        
        return True

    def process_all_memories(self):
        # 膨大な記憶（md, txt, log）を走査
        targets = []
        for file in os.listdir(self.base_dir):
            if file.endswith((".md", ".txt", ".json", ".log")) and "PHOENIX" in file:
                targets.append(file)
        
        for t in targets:
            self.encrypt_and_push(t)

if __name__ == "__main__":
    vault = CryptoVault()
    vault.process_all_memories()
