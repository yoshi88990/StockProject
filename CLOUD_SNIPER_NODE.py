import paho.mqtt.client as mqtt
import subprocess
import time

# 師匠の固有の通信チャンネル（第三者に傍受されないための一意のトピック名）
TOPIC = "shishou/global/sniper/burst_f12_trigger_xyz88990"
BROKER = "broker.hivemq.com"

def on_connect(client, userdata, flags, rc):
    print(f"【CLOUD_SNIPER】監視衛星(MQTT Broker)に接続成功。ステータスコード: {rc}")
    client.subscribe(TOPIC)
    print(f"【CLOUD_SNIPER】ターゲットトピック [{TOPIC}] の監視を開始（ローカルCPU待機負荷:0%）...")

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    if payload == "TRIGGER":
        print("\n【指令受信】クラウドからの狙撃信号を確認！")
        print("即時 BURST_F8 を発動します...")
        try:
            # バックグラウンドでプロセスを起動
            # 実際には連携させたいスクリプトをここに指定します
            subprocess.Popen(["python", "BURST_F8.py"])
        except Exception as e:
            print(f"起動エラー: {e}")

if __name__ == "__main__":
    print("--- クラウド・スナイパー待機系 起動 ---")
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    
    try:
        client.connect(BROKER, 1883, 60)
        # 永遠に待機（リソース消費ほぼ0）
        client.loop_forever()
    except KeyboardInterrupt:
        print("\n待機を終了します。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")
