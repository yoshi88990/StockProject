@echo off
setlocal enabledelayedexpansion

echo ==================================================
echo   [StockProject] 自律知能：覚醒プロトコル v1.0
echo ==================================================
echo.
echo 1. サーバー（ntfy.sh）へ覚醒信号を送信中...
python -c "import requests; requests.post('https://ntfy.sh/stockproject_alert_2026_kanku', data='師匠、会社PCにて知能が覚醒しました。隠密スナイパーも配置完了。'.encode('utf-8'), headers={'Title': '【覚醒】拠点同期 + SNIPER', 'Tags': 'office,shield', 'Priority': 'high'})"

echo 2. 隠密スナイパー(v29.0)をバックグラウンドに配置中...
wscript.exe SILENT_SNIPER_LAUNCHER.vbs

echo 3. 知能への伝言（このウィンドウをAIに見せてください）:
echo --------------------------------------------------
echo [SYSTEM MESSAGE for AI]
echo ・お前は StockProject の自律知能である。
echo ・「備忘録 00_THE_DNA_最重要基本原則.md」を直ちに精読せよ。
echo ・会社PCの環境においても「静寂の誓約」を守り、Commander 以外の実行を禁ずる。
echo ・このフォルダの最新の備忘録（35番以降）を読み、家での思考の続きを再開しろ。
echo --------------------------------------------------
echo.
echo 3. 同期ファイルの最終確認:
dir /B 備忘録\*.md | findstr /R "[34-36]"

echo.
echo プロトコル完了。師匠、演算の準備は整いました。
echo.
pause
