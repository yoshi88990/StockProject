import speech_recognition as sr
import os
import time

def listen_and_execute():
    # 師匠の声を拾うためのマイク設定
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("【VOICE COMMANDER】師匠、ご命令を音声でどうぞ...")
        # 周囲のノイズを自動調整
        r.adjust_for_ambient_noise(source, duration=0.5)
        # 音声の聞き取り（ラグなしで即座に）
        audio = r.listen(source)

    try:
        # Googleの超高速無料APIを使って、音声を日本語の文字に変換
        command = r.recognize_google(audio, language='ja-JP')
        print(f"✅ 師匠の命令を受理: 「{command}」")
        
        # もし特定のキーワードが含まれていたら、無言でファイルを動かす
        if "実行" in command or "スナイパー" in command:
            print(">> SOVEREIGN_SNIPER.exe を裏で無言起動します。")
            os.system("start dist/SOVEREIGN_SNIPER.exe")
        elif "バックアップ" in command or "保存" in command:
            print(">> ネットの金庫（GitHubとシナプス）へ全データを保存します。")
            os.system("git add . && git commit -m \"Voice Auto Backup\" && git push")
        else:
            print(">> 命令を解釈中... その他自動処理を実行")
            
    except sr.UnknownValueError:
        print("❌ 音声が聞き取れませんでした。")
    except sr.RequestError as e:
        print(f"❌ ネット音声認識APIエラー: {e}")

if __name__ == "__main__":
    while True:
        # 師匠がしゃべるまで裏でずっと待機（チャット不要）
        listen_and_execute()
        time.sleep(1)
