@echo off
setlocal
title PHOENIX EXTERNAL KILLER v1.1
mode con: cols=65 lines=18
color 0C

echo =============================================================
echo [PHOENIX EXTERNAL KILLER : 外部狙撃者排除プロトコル]
echo =============================================================
echo.
echo 現在、OSの深部で動作している可能性のある
echo すべての「狙撃手(Sniper)」および「番犬(Watchdog)」を強制終了します。
echo.
echo -------------------------------------------------------------

:: 1. pythonw.exe (バックグラウンドの狙撃手)
echo [1/3] 潜伏中の狙撃手(pythonw.exe)をスキャン中...
taskkill /F /IM pythonw.exe /T >nul 2>&1
if %errorlevel% equ 0 (
    echo    --^> 狙撃プロセスを捕捉・排除しました。
) else (
    echo    --^> 潜伏中の狙撃手は見つかりませんでした。
)

:: 2. python.exe (コンソール版の狙撃手)
echo [2/3] コンソール版狙撃手(python.exe)をスキャン中...
taskkill /F /IM python.exe /T >nul 2>&1
if %errorlevel% equ 0 (
    echo    --^> コンソールプロセスを排除しました。
)

:: 3. wscript.exe (ランチャー/自動復旧)
echo [3/3] 自動起動エンジン(wscript.exe)を停止中...
taskkill /F /IM wscript.exe /T >nul 2>&1
if %errorlevel% equ 0 (
    echo    --^> ランチャーを停止しました。
)

echo -------------------------------------------------------------
echo.
echo 【完了】外部スナイパーはすべて排除されました。
echo 安全が確保されました。
echo.
echo 何かキーを押すと閉じます。
pause > nul
