@echo off
set "PYTHON_EXE=..\python_embed\python.exe"
set "SCRIPT_PATH=DNA_SNIPER_APP.py"

if not exist "%PYTHON_EXE%" (
    echo [ERROR] python_embedが見つかりません。
    pause
    exit /b
)

title 👁️ DNA SNIPER
start "👁️ DNA SNIPER" "%PYTHON_EXE%" "%SCRIPT_PATH%" %1
exit
