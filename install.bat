@echo off
chcp 65001 >nul
cd /d "%~dp0"
python --version >nul 2>&1
if errorlevel 1 (
    echo [31mPython is not installed. Please install Python and ensure it is added to PATH[0m
    pause
    exit /b
)

if not exist requirements.txt (
    echo [31mRequirements.txt not found in the current directory[0m
    pause
    exit /b
)

echo Installing requirements from requirements.txt...
pip install -r requirements.txt
if errorlevel 1 (
    echo [31mFailed to install some requirements. Please check the errors above[0m
    pause
    exit /b
)

echo [32mRequirements installed Successfully (run main.py)[0m
pause