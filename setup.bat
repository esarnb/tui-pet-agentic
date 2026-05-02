@echo off
setlocal

echo Installing Python dependencies...
pip install -r "%~dp0requirements.txt"
if %errorlevel% neq 0 (
    echo ERROR: pip install failed. Make sure Python 3.10+ is installed.
    pause
    exit /b 1
)

echo.
echo Adding project directory to user PATH...
setx PATH "%PATH%;%~dp0"

echo.
echo ============================================================
echo  Setup complete!
echo
echo  IMPORTANT: Restart your terminal for PATH changes to take effect.
echo
echo  Then run:
echo    pet status       -- check your new pet
echo    launch.bat       -- open the live pet window
echo ============================================================
echo.
pause
endlocal
