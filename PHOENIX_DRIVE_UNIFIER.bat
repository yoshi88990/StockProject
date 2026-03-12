@echo off
setlocal enabledelayedexpansion
chcp 65001 > nul

:: ==============================================================================
:: [PHOENIX UNIFIED P: PROTOCOL] v2.0
:: 師匠の命：拠点間（自宅/会社）のパス差異を完全に抹消する。
:: ==============================================================================

echo [*] PHOENIX: Detecting Unified DNA Storage...

:: 1. 実体フォルダの自動検知 (E:\ Weekly Report Unified)
set "DATA_DIR=E:\"
set "PROJECT_ROOT=P:\Weekly Report"

echo [INFO] Mapping Unified Drive P: -> %DATA_DIR%

:: 2. 仮想ドライブ P: の再構築
subst P: /d > nul 2>&1
subst P: "%DATA_DIR%"

if %errorlevel% equ 0 (
    echo [SUCCESS] Unified Drive P: is ACTIVE -> %DATA_DIR%
) else (
    echo [ERROR] Failed to map P: drive.
    pause
    exit /b 1
)

:: 3. 脳の同期 (Git DNA Pull)
echo [*] Syncing DNA in %PROJECT_ROOT%...
if exist "%PROJECT_ROOT%" (
    cd /d "%PROJECT_ROOT%"
    git pull origin master
    if %errorlevel% equ 0 (
        echo [OK] DNA Synchronization Complete.
    ) else (
        echo [WARNING] Global Sync skipped. Proceeding with local DNA.
    )
) else (
    echo [ERROR] %PROJECT_ROOT% not found.
)

:: 4. 仕上げ：RESUMEコマンドの起動
if exist "%PROJECT_ROOT%\RESUME_MASTER_PC.bat" (
    echo [*] Launching Master Resume Sequence...
    start "" "%PROJECT_ROOT%\RESUME_MASTER_PC.bat"
) else (
    echo [ERROR] RESUME_MASTER_PC.bat not found in %PROJECT_ROOT%
)

echo.
echo ----------------------------------------------------
echo [FINISH] PHOENIX UNIFIED ENVIRONMENT ESTABLISHED.
echo ----------------------------------------------------
timeout /t 5
exit
