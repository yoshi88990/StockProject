@echo off
setlocal
title 🚨 PHOENIX EMERGENCY STOP 🚨
mode con: cols=70 lines=22
color 0C

echo ==============================================================
echo  [ 🚨 PHOENIX 緊急停止プロトコル: 強制排除 🚨 ]
echo ==============================================================
echo.
echo  このプログラムは、動作中のすべてのスナイパー・監視プロセスを
echo  OSレベルで強制的に、かつ即座に終了させます。
echo.
echo  ★自宅PC・会社PCの両方で、スナイパーが暴走した際に使用してください。
echo.
echo  ------------------------------------------------------------
echo  [実行中...]
echo.

:: 繰り返し殺すことで、再起動しようとするプロセスを確実に仕留める
for /L %%i in (1,1,3) do (
    echo  [Pass %%i] 狙撃プロセスをスキャン中...
    taskkill /F /IM pythonw.exe /T >nul 2>&1
    taskkill /F /IM python.exe /T >nul 2>&1
    taskkill /F /IM wscript.exe /T >nul 2>&1
    taskkill /F /IM cscript.exe /T >nul 2>&1
    timeout /t 1 /nobreak >nul
)

echo.
echo  ------------------------------------------------------------
echo  【完了】すべての PHOENIX プロセスは消失しました。
echo.
echo  マウス/キーボードの制御は解放されました。
echo.
echo  何かキーを押すとこの画面を閉じます。
pause > nul
