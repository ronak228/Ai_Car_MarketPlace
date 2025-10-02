#!/bin/bash

echo "🚀 Starting Car Price Predictor with Market Trends..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo "❌ Python is not installed"
    echo "Please install Python 3.8+ and try again"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed"
    echo "Please install Node.js 14+ and try again"
    exit 1
fi

# Check if required files exist
if [ ! -f "unified_app.py" ]; then
    echo "❌ unified_app.py not found"
    exit 1
fi

if [ ! -f "client/package.json" ]; then
    echo "❌ client/package.json not found"
    exit 1
fi

echo "✅ Prerequisites check passed"
echo ""

# Use python3 if available, otherwise python
PYTHON_CMD="python3"
if ! command -v python3 &> /dev/null; then
    PYTHON_CMD="python"
fi

echo "🔧 Starting Flask Server (Port 5000)..."
$PYTHON_CMD unified_app.py &
FLASK_PID=$!

echo "⏳ Waiting for Flask server to start..."
sleep 8

echo "🌐 Starting React Development Server (Port 3000)..."
cd client
npm start &
REACT_PID=$!
cd ..

echo ""
echo "✅ Both servers are running!"
echo ""
echo "📱 Access your application:"
echo "   🌐 React App: http://localhost:3000"
echo "   🔧 Flask API: http://localhost:5000"
echo "   📊 Market Trends: http://localhost:3000/market-trends (after login)"
echo ""
echo "🔑 For development login, use any email and any 6-digit OTP"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for user to stop
trap "echo 'Stopping servers...'; kill $FLASK_PID $REACT_PID 2>/dev/null; exit" INT
wait
