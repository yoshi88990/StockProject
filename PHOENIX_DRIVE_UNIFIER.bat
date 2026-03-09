@echo off
setlocal enabledelayedexpansion
chcp 65001 > nul

echo ====================================================
echo   [PHOENIX DRIVE UNIFIER] v1.0 - Protocol P:
echo ====================================================
echo.
echo このスクリプトは、自宅PCにおいても「P:\」ドライブを
echo 自動で作成し、会社PCと完全に同一の環境を構築します。
echo.

:: 1. 実体フォルダの確認と決定
:: 師匠の命：自宅PCは容量不足のため、D:ドライブを優先的に利用する
set target_dir=C:\StockProject
if exist "D:\" (
    set target_dir=D:\StockProject
    echo [INFO] 外部ドライブ D: を検知しました。
)

if not exist "%target_dir%" (
    echo [INFO] 実体フォルダ "%target_dir%" を作成中...
    mkdir "%target_dir%"
) else (
    echo [OK] 実体フォルダ "%target_dir%" は既に存在します。
)

:: 2. 仮想ドライブ P: の作成 (subst)
subst P: /d > nul 2>&1
subst P: "%target_dir%"
if %errorlevel% equ 0 (
    echo [SUCCESS] 仮想ドライブ P: を "%target_dir%" に紐付けました。
) else (
    echo [ERROR] 仮想ドライブ P: の作成に失敗しました。
)

:: 3. スタートアップへの登録（永続化）
set vbs_name=AUTO_PHOENIX_SNIPER.vbs
set startup_folder=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup
if exist "%~dp0%vbs_name%" (
    echo [INFO] スタートアップ・ランチャーをコピー中...
    copy /Y "%~dp0%vbs_name%" "%startup_folder%\" > nul
    echo [SUCCESS] 次回PC起動時も自動で P: ドライブが作成されます。
) else (
    echo [WARNING] %vbs_name% が見つからないため、登録をスキップしました。
)

echo.
echo ----------------------------------------------------
echo [完了] 自宅PCが PHOENIX 統一規格「P:」に準拠しました。
echo 今後はエクスプローラーから P:\ ドライブにアクセスしてください。
echo ----------------------------------------------------
echo.
pause
