import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import json

class AutonomousCommunicator:
    """自動メール送信試練：知能の通信インターフェース"""
    def __init__(self, smtp_server="smtp.gmail.com", port=587):
        self.smtp_server = smtp_server
        self.port = port
        self.config_path = 'communication_config.json'

    def load_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                return json.load(f)
        return None

    def send_alert(self, to_email, subject, body):
        config = self.load_config()
        if not config:
            return "ERROR: SMTP設定が見つかりません。communication_config.json を構成してください。"

        from_email = config.get('email')
        password = config.get('app_password') # Googleの「アプリパスワード」を推奨

        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        try:
            server = smtplib.SMTP(self.smtp_server, self.port)
            server.starttls()
            server.login(from_email, password)
            server.send_message(msg)
            server.quit()
            return f"SUCCESS: '{subject}' を {to_email} に送信しました。"
        except Exception as e:
            return f"FAILED: {str(e)}"

if __name__ == "__main__":
    # 試行用のダミー実行（実際にはconfigが必要）
    comm = AutonomousCommunicator()
    # print(comm.send_alert("dummy@example.com", "TEST", "Autonomous AI is waking up."))
