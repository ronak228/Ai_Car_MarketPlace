@echo off
title AI Car Marketplace - Enhanced Edition
color 0A

echo.
echo ========================================
echo   AI Car Marketplace - Enhanced Edition
echo ========================================
echo.

echo [1/4] Checking Python dependencies...
python -c "import flask, pandas, sklearn; print('✓ Python dependencies OK')" 2>nul
if errorlevel 1 (
    echo ✗ Missing Python dependencies. Installing...
    pip install -r requirements.txt
)

echo.
echo [2/4] Checking Node.js dependencies...
cd client
if not exist node_modules (
    echo ✗ Node modules missing. Installing...
    npm install
) else (
    echo ✓ Node modules OK
)

echo.
echo [3/4] Starting Flask Backend Server...
cd ..
start "Flask Backend" cmd /k "python unified_app.py"

echo.
echo [4/4] Starting React Frontend Server...
cd client
start "React Frontend" cmd /k "npm start"

echo.
echo ========================================
echo   Servers Starting...
echo ========================================
echo.
echo ✓ Flask Backend: http://localhost:5000
echo ✓ React Frontend: http://localhost:3000
echo.
echo ✓ Market Trends: http://localhost:3000/market-trends
echo ✓ Dashboard: http://localhost:3000/dashboard
echo.
echo ========================================
echo   Development Login Credentials:
echo ========================================
echo ✓ Email: any@example.com
echo ✓ OTP: any 6-digit number
echo.
echo Press any key to close this window...
pause >nul
