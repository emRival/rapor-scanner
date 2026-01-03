@echo off
REM Rapor Scanner - Update Script for Windows

set APP_DIR=%USERPROFILE%\rapor-scanner

echo.
echo ========================================================
echo        Rapor Scanner - Update
echo ========================================================
echo.

cd /d "%APP_DIR%" || (
    echo ERROR: Directory not found: %APP_DIR%
    pause
    exit /b 1
)

echo Pulling from GitHub...
git pull origin main

echo Updating dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt -q

echo.
echo Update complete!
echo.
echo To run: double-click run.bat
echo.
pause
