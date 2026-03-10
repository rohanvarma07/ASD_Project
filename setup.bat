@echo off
REM ========================================
REM ASD Detection System - Quick Start Script (Windows)
REM ========================================

echo ==========================================
echo ASD DETECTION SYSTEM - SETUP
echo ==========================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo ✓ Python found

REM Create virtual environment
echo.
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo.
echo ==========================================
echo ✓ SETUP COMPLETE!
echo ==========================================
echo.
echo To start the application:
echo 1. Activate virtual environment: venv\Scripts\activate.bat
echo 2. Run the app: python app.py
echo 3. Open browser: http://localhost:5000
echo.
echo Test credentials:
echo Email: admin@example.com
echo Password: admin123
echo.
echo ==========================================
pause
