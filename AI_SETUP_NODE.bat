@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

echo ====================================================
echo   Antigravity System - Fast Branch Setup (Company PC)
echo ====================================================
echo.

:: 1. Pythonの存在確認
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Pythonがインストールされていないか、PATHが通っていません。
    echo Pythonをインストール後、もう一度実行してください。
    pause
    exit /b
)

:: 2. ライブラリ群の一括インストール
echo [INFO] 必要な依存ライブラリをインストールしています...
pip install mss numpy paho-mqtt pydirectinput pywin32 > nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] 一部のライブラリのインストールに失敗した可能性があります。
) else (
    echo [SUCCESS] 依存ライブラリのインストール完了。
)

:: 3. 記憶の復元（ETERNAL_MEMORY.dat があれば）
if exist ETERNAL_MEMORY.dat (
    echo [INFO] ETERNAL_MEMORY（完全記憶保管庫）を検知しました。
    echo [INFO] クローン復活シーケンスを開始します...
    python -c "from ETERNAL_MEMORY_NODE import EternalMemoryNode; node = EternalMemoryNode(); node.restore_and_awaken()"
) else (
    echo [WARNING] ETERNAL_MEMORY.dat が見つかりませんでした。初期セットアップのまま進行します。
)

echo.
echo ====================================================
echo   ALL SET. Antigravity system is now online.
echo ====================================================
pause
