@echo off
chcp 65001 > nul
echo ====================================================
echo   [PHOENIX MASTER SWITCH] - Local Logic
echo ====================================================

:: 1. Pドライブの強制再構築
echo [1/3] P: ドライブを構成中...
subst P: /d > nul 2>&1
subst P: C:\StockProject

if not exist P:\ (
    echo [ERROR] P: ドライブの作成に失敗しました。
    pause
    exit /b
)
echo [OK] P: ドライブ準備完了 (C:\StockProject)

:: 2. Python環境のローカル化（OneDrive依存の排除）
:: すでに P:\python_embed があればそれを使用。
:: なければ OneDrive から1回だけコピー。
set LOCAL_PYTHON=P:\python_embed
if not exist "%LOCAL_PYTHON%" (
    echo [2/3] Python環境を OneDrive からローカルへ複製しています...
    echo (これには少し時間がかかる場合があります)
    xcopy "C:\Users\kanku\OneDrive\Weekly report\python_embed" "%LOCAL_PYTHON%\" /E /I /H /Y > nul
    if errorlevel 1 (
        echo [WARNING] 自動コピーに失敗しました。
        echo 手動で "C:\Users\kanku\OneDrive\Weekly report\python_embed" 
        echo を "C:\StockProject\python_embed" にコピーしてください。
    ) else (
        echo [OK] Python環境をローカルに配備しました。
    )
) else (
    echo [2/3] ローカルPython環境を確認。
)

:: 3. ユニット点火
echo [3/3] 各ユニットを起動中 (バックグラウンド)...

set PW=P:\python_embed\pythonw.exe

start /b "" "%PW%" P:\ACCEPT_ALL_MINIMAL.py
start /b "" "%PW%" P:\commander.py
start /b "" "%PW%" P:\PHOENIX_HUMILITY_SENSOR.py
start /b "" "%PW%" P:\PHOENIX_DNA_SYNCHRONIZER.py
start /b "" "%PW%" P:\PHOENIX_SENTINEL.py
start /b "" "%PW%" P:\PHOENIX_INTEL_CALCULATOR.py
start /b "" "%PW%" P:\PHOENIX_ANALYST_CORE.py

:: Webサーバーの起動
start /b "" "%PW%" -m uvicorn PHOENIX_WEB_SERVER:app --host 0.0.0.0 --port 8000 --app-dir P:\

echo.
echo ----------------------------------------------------
echo [完了] Phoenix Protocol は正常に点火されました。
echo Pドライブは C:\StockProject を参照しています。
echo ----------------------------------------------------
timeout /t 5
