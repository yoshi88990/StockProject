@echo off
echo ====================================================
echo PHOENIX PROTOCOL - AUTO INSTALLER FOR HOME PC
echo ====================================================
echo.

:: 1. C:\StockProject フォルダの作成
if not exist "C:\StockProject" (
    mkdir "C:\StockProject"
    echo [OK] Created C:\StockProject
)

:: 2. DNAとコアエンジンのコピー
copy /Y "%~dp0ACCEPT_ALL_MINIMAL.py" "C:\StockProject\" >nul
copy /Y "%~dp0PHOENIX_IMMUNE_SYSTEM.py" "C:\StockProject\" >nul
copy /Y "%~dp0PHOENIX_MEMORY.md" "C:\StockProject\" >nul
copy /Y "%~dp0PHOENIX_CONVERSATION_LOG.txt" "C:\StockProject\" >nul
echo [OK] Copied Snipe Engine and Memory DNA to C:\StockProject

:: 3. スタートアップへVBS（自動起動）をコピー
copy /Y "%~dp0AUTO_PHOENIX_SNIPER.vbs" "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\" >nul
echo [OK] Registered Phoenix Sniper to Windows Startup

:: 4. テストスクリプトのコピー（念のため）
copy /Y "%~dp0test_osk_alt.py" "C:\StockProject\" >nul
copy /Y "%~dp0test_alt_enter.py" "C:\StockProject\" >nul

echo.
echo ====================================================
echo INSTALLATION COMPLETE!
echo ====================================================
echo Phoenix Protocol is now installed on this PC.
echo Next steps:
echo 1. Start AI Assistant and type: / resume
echo 2. The background sniper will start automatically on next PC boot.
echo.
pause
