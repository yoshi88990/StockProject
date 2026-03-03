import win32api
import time
import datetime
import os

class MasterOverrideListener:
    """
    【師匠の物理介入（F8）検知システム】
    AIが「送信して成功したつもりになっている」独りよがりな状態を防ぐため、
    「実際に師匠が物理キーボードでF8を押したか」を常時監視します。
    もし師匠がF8を押した場合、それは「AIの打鍵が失敗した（弾かれた）ため師匠がカバーしてくれた」
    という事実としてログに刻み、AIの自己反省（パラメーター修正）を促します。
    """
    def __init__(self):
        self.log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Weekly Report", "Master_Override_Log.txt")

    def listen_for_f8(self):
        print("【MASTER_OVERRIDE_LISTENER】 師匠の物理的な「F8」打鍵の監視を開始しました。")
        print("AIの不甲斐なさにより師匠にF8を押させてしまった場合、それを検知・記録します。")
        
        VK_F8 = 0x77
        was_pressed = False
        
        try:
            while True:
                # GetAsyncKeyState は物理的なキーの押下状態をOSの最下層から拾う
                state = win32api.GetAsyncKeyState(VK_F8)
                is_pressed = (state & 0x8000) != 0
                
                if is_pressed and not was_pressed:
                    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    msg = f"\n[{timestamp}] 【検知】 師匠による物理的な『F8』入力を確認しました。"
                    print(msg)
                    print(" -> AIの自動打鍵が機能せず、師匠に手動で介入させてしまった事実をシステムに記録します。")
                    
                    with open(self.log_file, "a", encoding="utf-8") as f:
                        f.write(msg + " (AUTOMATION FAILED - MASTER INTERVENED)\n")
                    
                    was_pressed = True
                elif not is_pressed and was_pressed:
                    was_pressed = False
                    
                time.sleep(0.05)
        except KeyboardInterrupt:
            print("監視機能を停止します。")

if __name__ == "__main__":
    listener = MasterOverrideListener()
    listener.listen_for_f8()
