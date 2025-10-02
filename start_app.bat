@echo off
echo 🚀 Starting Car Price Predictor with Market Trends...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js is not installed or not in PATH
    echo Please install Node.js 14+ and try again
    pause
    exit /b 1
)

REM Check if required files exist
if not exist "unified_app.py" (
    echo ❌ unified_app.py not found
    pause
    exit /b 1
)

if not exist "client\package.json" (
    echo ❌ client\package.json not found
    pause
    exit /b 1
)

echo ✅ Prerequisites check passed
echo.

echo 🔧 Starting Flask Server (Port 5000)...
start "Flask Server - Car Price Predictor" cmd /k "python unified_app.py"

echo ⏳ Waiting for Flask server to start...
timeout /t 8 /nobreak > nul

echo 🌐 Starting React Development Server (Port 3000)...
start "React Client - Car Price Predictor" cmd /k "cd client && npm start"

echo.
echo ✅ Both servers are starting!
echo.
echo 📱 Access your application:
echo    🌐 React App: http://localhost:3000
echo    🔧 Flask API: http://localhost:5000
echo    📊 Market Trends: http://localhost:3000/market-trends (after login)
echo.
echo 🔑 For development login, use any email and any 6-digit OTP
echo.
echo Press any key to close this window...
pause > nul
