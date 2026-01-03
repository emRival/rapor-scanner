@echo off
REM Rapor Scanner - Installation Script for Windows
REM 
REM Usage: Run as Administrator
REM   1. Download this file
REM   2. Right-click > Run as Administrator

echo.
echo ========================================================
echo        Rapor Scanner - Windows Installation
echo ========================================================
echo.

set APP_DIR=%USERPROFILE%\rapor-scanner
set REPO_URL=https://github.com/emRival/rapor-scanner.git

REM Check Python
echo [1/5] Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found!
    echo Please install Python from https://python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)
echo OK: Python found

REM Check Git
echo [2/5] Checking Git...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Git not found!
    echo Please install Git from https://git-scm.com
    pause
    exit /b 1
)
echo OK: Git found

REM Clone repository
echo [3/5] Cloning repository...
if exist "%APP_DIR%" (
    cd /d "%APP_DIR%"
    git pull origin main
) else (
    git clone %REPO_URL% "%APP_DIR%"
    cd /d "%APP_DIR%"
)

REM Create virtual environment
echo [4/5] Setting up Python environment...
python -m venv venv
call venv\Scripts\activate.bat
pip install --upgrade pip -q
pip install -r requirements.txt

REM Create run script
echo [5/5] Creating run script...
(
echo @echo off
echo cd /d "%%~dp0"
echo call venv\Scripts\activate.bat
echo streamlit run app.py --server.port 8501
echo pause
) > "%APP_DIR%\run.bat"

echo.
echo ========================================================
echo        Installation Complete!
echo ========================================================
echo.
echo Location: %APP_DIR%
echo.
echo To Run:
echo   Double-click: %APP_DIR%\run.bat
echo.
echo Access: http://localhost:8501
echo.
echo ========================================================
echo.
echo IMPORTANT: Install Poppler for OCR support:
echo   1. Download from: https://github.com/oschwartz10612/poppler-windows/releases
echo   2. Extract to C:\poppler
echo   3. Add C:\poppler\bin to System PATH
echo.
pause
