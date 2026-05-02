@echo off
setlocal

set SCRIPT_DIR=%~dp0
set TITLE=Terminal Pet

:: Try Windows Terminal first
where wt >nul 2>&1
if %errorlevel% == 0 (
    start "" wt -w 0 nt --title "%TITLE%" --size 42,22 cmd /k "cd /d \"%SCRIPT_DIR%\" && python pet_window.py"
    goto :done
)

:: Fall back to a plain cmd window
start "%TITLE%" cmd /k "cd /d \"%SCRIPT_DIR%\" && python pet_window.py"

:done
endlocal
