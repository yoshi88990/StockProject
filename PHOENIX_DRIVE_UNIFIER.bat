@echo off
setlocal enabledelayedexpansion
chcp 65001 > nul

:: ==============================================================================
:: [PHOENIX UNIFIED P: PROTOCOL] v2.0
:: 師匠の命：拠点間（自宅/会社）のパス差異を完全に抹消する。
:: ==============================================================================

echo [*] PHOENIX: Detecting Unified DNA Storage...

:: 1. 実体フォルダの自動検知 (Home vs Office)
:: D:\ を優先し、なければ C:\ を探索する。
set "BASE_NAME=StockProject"
set "DATA_DIR=C:\%BASE_NAME%"

if exist "D:\%BASE_NAME%" (
    set "DATA_DIR=D:\%BASE_NAME%"
    echo [INFO] Detected: Home PC Pattern (Drive D:)
) else (
    echo [INFO] Detected: Office PC Pattern (Drive C:)
)

:: 2. 仮想ドライブ P: の再構築
subst P: /d > nul 2>&1
subst P: "%DATA_DIR%"

if %errorlevel% equ 0 (
    echo [SUCCESS] Unified Drive P: is ACTIVE -> %DATA_DIR%
) else (
    echo [ERROR] Failed to map P: drive. Please check if P: is already in use.
    pause
    exit /b 1
)

:: 3. 脳の同期 (Git DNA Pull)
echo [*] Syncing DNA with Global Cloud...
cd /d P:\
git pull origin master
if %errorlevel% equ 0 (
    echo [OK] DNA Synchronization Complete.
) else (
    echo [WARNING] Global Sync skipped. Proceeding with local DNA.
)

:: 4. 仕上げ：RESUMEコマンドの起動
if exist "P:\RESUME_MASTER_PC.bat" (
    echo [*] Launching Master Resume Sequence...
    start "" "P:\RESUME_MASTER_PC.bat"
) else (
    echo [ERROR] RESUME_MASTER_PC.bat not found on P:
)

echo.
echo ----------------------------------------------------
echo [FINISH] PHOENIX UNIFIED ENVIRONMENT ESTABLISHED.
echo ----------------------------------------------------
timeout /t 5
exit
