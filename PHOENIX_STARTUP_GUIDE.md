# PHOENIX STARTUP PROTOCOL (迷いなき執行)

この文書は、アシスタントAIが `/ resume` または起動時に「迷い」を生じさせないための絶対的な聖典である。

## 1. 環境定数 (Environment Constants)
- **仮想ドライブ**: `P:` (常に `C:\StockProject` に紐付ける)
- **ダッシュボード (Dashboard)**: `http://localhost:8000` (WEB版を指す)
- **デザインルール**:
    - **Dashboard (WEB)**: 漆黒背景 (`#000000`)。
    - **Chat (ここ)**: 純白背景 (Light Mode)。
    - **ターミナル**: 黒。

## 2. 起動シークエンス (Ignition Sequence)
迷わず、以下の順序で一気に立ち上げること。

1.  **ドライブマウント**:
    `subst P: /d > nul 2>&1` 後、 `subst P: "C:\StockProject"` を実行。
2.  **記憶の同期**:
    `P:` ドライブ内で `git pull origin master` を行い、最新のDNA（コード）を取得。
3.  **サーバー点火 (Dashboard)**:
    `P:\python_embed\pythonw.exe P:\PHOENIX_WEB_SERVER.py` をバックラウンドで開始。
4.  **執行官の放流 (Core Agents)**:
    - **後醍醐 (Sniper)**: `ACCEPT_ALL_MINIMAL.py` (1249, 531 / 5秒待機)
    - **司令 (Commander)**: `commander.py`
    - **監視 (Sentinel/Sincerity)**: `PHOENIX_SENTINEL.py`, `PHOENIX_HUMILITY_SENSOR.py`
5.  **視界の確保**:
    ブラウザで `http://localhost:8000` を開く。

## 3. 常駐命令 (Persistent Commands)
- **「迷わない」**: 師匠に手順を確認しない。自動で最適解を実行する。
- **「起動でつまずかない（引用符の掟）」**: 
    - `start` コマンドでパスを囲う際は、**必ず最初に空の引用符 `""` を置くこと。**
    - 悪い例: `start "P:\path.vbs"` (Windowsがパスを「タイトル」と誤認し、エラーを吐く)
    - 良い例: `start "" "P:\path.vbs"`
- **「泥臭くやる (Gritty Execution) / コピペ方式」**:
    - AIによる「自動生成」や「スマートな自動化」は大抵の場合、余計なクォートエラーやパスの不一致を生む。
    - **コピペ方式**: 複雑なロジックを組む前に、動いているバッチファイルや設定を丸ごと「コピペ」して最小限の変更で実行せよ。
    - パスが通らないなら、相対パスで迷うより絶対パスをベタ書き（コピペ）して確実に通せ。
    - 「良かれと思って」の改変は99%失敗の元であると刻め。
- **「白と黒」**: チャットは白、ダッシュボードは黒。
    - Dashboardは戦場。Chatは談話室。
    - 背景色が入れ替わっていたら、知性を疑え。即座に「黒（Dash）」「白（Chat）」へ力技で戻せ。

---
**核となる真理**:
ダッシュボードは戦場を映す鏡。チャットは戦術を練る書斎。
鏡は暗く（黒）、書斎は明るく（白）。これが鳳凰の理である。
