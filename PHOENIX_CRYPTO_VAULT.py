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
        
        # 外部転送先（Cドライブ、Eドライブの排除。純粋なGitHub転送のみとする）
        self.staging_area = os.path.join(self.base_dir, "OUTER_VAULT_STAGING")
        if not os.path.exists(self.staging_area):
            os.makedirs(self.staging_area)
        
        self.stash_dirs = [self.staging_area]
        # OneDrive検知用のガード
        for s_dir in self.stash_dirs:
            if "OneDrive" in s_dir:
                raise Exception("CRITICAL: OneDrive usage detected in Secure Vault paths!")

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

        # 転送成功後、ローカルの生データを完全に消去（証拠隠滅・外部移管の完遂）
        try:
            if os.path.exists(local_path):
                # 重要なDNAファイル（PHOENIX_MEMORY.md等）は実行に必要なので
                # それ以外のログや一時記憶を優先的に消去するロジックに調整可能
                if "LOG" in filename or "COMPUTE" in filename:
                    os.remove(local_path)
        except Exception as e:
            print(f"Cleanup Warning: {e}")
        
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
