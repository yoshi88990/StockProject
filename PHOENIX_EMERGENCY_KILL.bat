@echo off
title PHOENIX EMERGENCY KILL SWITCH
mode con: cols=60 lines=15
color 0C

echo ==========================================
echo [PHOENIX EMERGENCY KILL SWITCH]
echo nXiCp[̋rJn܂...
echo ==========================================
echo.

:: PythonvZXSďI
echo [1/3] PythonProcesses (pythonw.exe) Jbg܂...
taskkill /F /IM pythonw.exe /T 2>nul

echo [2/3] Python Console (python.exe) Jbg܂...
taskkill /F /IM python.exe /T 2>nul

:: VBScript`[I
echo [3/3] Launchers (wscript.exe) Jbg܂...
taskkill /F /IM wscript.exe /T 2>nul

echo.
echo ------------------------------------------
echo ׂĂ PHOENIX vZX~܂B
echo ׂĂ̏錇͑Sɓh܂B
echo ------------------------------------------
echo.
echo Iɂ͂L[ĂB
pause > nul
