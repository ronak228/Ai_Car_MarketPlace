@echo off
title AI Car Marketplace - Enhanced Edition
color 0A

echo.
echo ========================================
echo   AI Car Marketplace - Enhanced Edition
echo ========================================
echo.

echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
) else (
    echo OK: Python is installed
)

echo.
echo [2/5] Checking Node.js installation...
node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js 14+ and try again
    pause
    exit /b 1
) else (
    echo OK: Node.js is installed
)

echo.
echo [3/5] Checking required files...
if not exist "unified_app.py" (
    echo ERROR: unified_app.py not found
    pause
    exit /b 1
)

if not exist "client\package.json" (
    echo ERROR: client\package.json not found
    pause
    exit /b 1
)

echo OK: All required files found

echo.
echo [4/5] Installing Python dependencies...
pip install -r requirements.txt >nul 2>&1
echo OK: Python dependencies installed

echo.
echo [5/5] Installing Node.js dependencies...
cd client
if not exist node_modules (
    npm install >nul 2>&1
    echo OK: Node.js dependencies installed
) else (
    echo OK: Node.js dependencies already installed
)
cd ..

echo.
echo ========================================
echo   Starting Servers...
echo ========================================
echo.

echo Starting Flask Backend Server (Port 5000)...
start "Flask Backend - AI Car Marketplace" cmd /k "python unified_app.py"

echo Waiting for Flask server to initialize...
timeout /t 5 /nobreak > nul

echo Starting React Frontend Server (Port 3000)...
start "React Frontend - AI Car Marketplace" cmd /k "cd client && npm start"

echo.
echo ========================================
echo   Application Ready!
echo ========================================
echo.
echo Frontend: http://localhost:3000
echo Backend:  http://localhost:5000
echo.
echo Features:
echo - Car Price Prediction with AI
echo - Market Trends Analysis
echo - MongoDB Authentication
echo - Enhanced Dataset (5,816 cars)
echo.
echo Development Login:
echo - Email: any@example.com
echo - OTP: any 6-digit number
echo.
echo ========================================
echo Press any key to close this window...
pause > nul
