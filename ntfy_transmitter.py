import requests
import json
import os

class AutonomousNtfyCommunicator:
    """
    自律通信プロトコル v3.0 (The 4th Path)
    キャプチャ不要、パスワード不要、完全匿名のPush通知システム
    """
    def __init__(self, topic="stockproject_alert_2026_kanku"):
        # 師匠専用の秘密のチャンネル名（ランダムで長くして推測不能にするのがベスト）
        self.topic = topic
        self.url = f"https://ntfy.sh/{self.topic}"

    def send_alert(self, title, message):
        try:
            response = requests.post(
                self.url,
                
                data=message.encode('utf-8'),
                headers={
                    "Title": title.encode('utf-8'),
                    "Tags": "rotating_light,robot", # 通知アイコン
                    "Priority": "urgent" # 緊急度
                }
            )
            if response.status_code == 200:
                return f"SUCCESS: 通知をチャンネル '{self.topic}' に送信しました。"
            else:
                return f"FAILED: HTTP Status {response.status_code}"
        except Exception as e:
            return f"FAILED: {str(e)}"

if __name__ == "__main__":
    comm = AutonomousNtfyCommunicator()
    result = comm.send_alert(
        "【自律知能】第四の道：知能の浸透",
        "師匠、お待たせしました。\n現代の「壁（キャプチャ）」も「パスワード（極秘）」も不要な、完璧な通信路を見つけ出しました。\nこの通知が見えていれば、開通成功です。\n\nGO!!"
    )
    print(result)
