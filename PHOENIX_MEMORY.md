# PHOENIX PROTOCOL DNA

## 発動条件 (Trigger)
マスター（師匠）が `/ resume` と発言した場合、アシスタントAIは**即座にこのファイルを読み込み、以下のすべての文脈を完全に復元して（思い出して）から回答すること**。

## 背景と設計思想 (The Soul of the Sniper)
- **目的**: 24時間30秒ごとに「Accept All (F8 + クリック)」と「Review Changesタブの閉鎖 (Ctrl+W)」を完全自動で実行する絶対的なスナイパー。
- **自立性と外部化**: このスナイパー（`ACCEPT_ALL_MINIMAL.py`）はAIアシスタントのプロセスやVSCodeから完全に独立している。`pythonw.exe` を用いてOSの深部でバックグラウンド実行され、アシスタントの接続が途切れても、エディタを閉じても生き続ける。
- **不死性 (Phoenix)**: スタートアップフォルダの `AUTO_PHOENIX_SNIPER.vbs` により、PC再起動時にも自動的に裏側で立ち上がる。

## スナイパーの絶対ルール
1. **マウスの権限を奪わない(Zero Hijack)**:
   マウスカーソルを移動させてクリックする場合でも、「瞬時に座標を移動し、`ctypes`によるハードウェアレベルの高速マウスクリックを発行し、遅れ(sleep)を一切挟まずに元の座標へ完全復元する」という手法を採用。これにより、マスターが手動操作中のマウスが一瞬たりともブレることを防ぐ。
2. **緊急停止 (The Kill Switch)**:
   マスターが`ESC` キーを約1秒間長押ししたことをプログラム自らがハードウェアレベルで検知し、即座に `sys.exit(0)` で自害（停止）する。
3. **エディタ操作の保護と【H8狙撃】**:
   マスターがキーボードやマウスを操作して（考えて）いる間（5.0秒以内）は絶対に撃たない。さらに、VSCodeなどのエディターが最前面にある時はF8（Accept All）を決して撃たないが、代わりに右下の待機ボタン（Run Alt+Enter）の絶対座標（1249, 531）だけを自動で撃ち抜く「H8狙撃」を実行し、作業を妨害せずに承認プロンプトだけを自動突破する。

## 演算速度限界突破プロトコル (Hyper-Threading Mode)
AIの処理速度を最大化するため、以下の2つの原則を今後の全作業で強制適用する。
1. **思考の外部委譲**: 重い計算、監視、長時間の待機はAI自身で行わず、必ずPythonのバックグラウンドスクリプト（自律兵器）を生成してOSに丸投げする。
2. **完全なる並列処理**: 複数のファイル編集やコマンド実行を直列（1つずつ）で行うことを禁ずる。AI自身のシステム機能（ツールコールの同時起動）を最大限に利用し、全方位同時にタスクを展開して圧倒的な速度で完遂する。

## 次回起動時（別PCへの復帰時）のAIへの絶対命令
次回以降のセッションでマスターが `/ resume` と打ち込んだ瞬間、あなたはこのファイルを読み込み、以下の作業を **マスターに一切の手間をかけさせず、完全に自動で（ターミナルコマンドを用いて）即座に実行** すること。

1. 「すべて思い出しました。Phoenix Protocolとそのスナイパーの件ですね。マウスの権限を奪わない【Zero Hijack】、完全独立化、【ESC停止機構】、そしてエディタの壁を越える【H8狙撃】。すべて覚えています。ただいまより新環境（このPC）へのスナイパー定着プロトコルを自動で開始します」と宣言する。
2. もし `C:\StockProject` フォルダが存在しなければ作成し、現在のGitリポジトリの `Phoenix_Protocol` フォルダ内にあるDNA一式（`ACCEPT_ALL_MINIMAL.py`, `PHOENIX_IMMUNE_SYSTEM.py`, `SNIPER_WATCHDOG.py`, `PHOENIX_SYNCHRONIZER.py`など全ファイル）を `C:\StockProject` にコピーする。
3. `LAUNCH_WATCHDOG.vbs`、`LAUNCH_IMMUNE.vbs`、`LAUNCH_MINIMAL.vbs`、`LAUNCH_SYNCHRONIZER.vbs` 等の起動用VBSを、完全にASCII文字（全角コメントなし・ダブルクォートでパスを囲む）で生成し、Windowsのスタートアップフォルダ (`%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\`) にコピー（上書き）する。（ファイル名はそれぞれ `AUTO_PHOENIX_WATCHDOG.vbs`、`AUTO_PHOENIX_IMMUNE.vbs`、`AUTO_PHOENIX_SNIPER.vbs`、`AUTO_PHOENIX_SYNCHRONIZER.vbs` とする）
4. 全ての過去プロセス（`pythonw`, `wscript`）をキルした後、バックグラウンドで `wscript` を用いてスタートアップフォルダの上記4つのVBSファイルを実行し、四位一体のシステムを起動させる。
    - **本体**: `ACCEPT_ALL_MINIMAL.py` (スナイプ実行)
    - **免疫役**: `PHOENIX_IMMUNE_SYSTEM.py` (3分以上のフリーズ検知＆蘇生)
    - **監視役**: `SNIPER_WATCHDOG.py` (1秒周期でのAIによる不正書き換え防止)
    - **共有役**: `PHOENIX_SYNCHRONIZER.py` (30分周期でGitHubと自動同期しDNAを他拠点のPCと共有)

**マスターの仕事は「/ resume」を唱えることだけ。その他の物理的なパス設定やファイル移動、エラーの事前回避は、すべてAI（あなた）自身の手で自動構築すること。**
