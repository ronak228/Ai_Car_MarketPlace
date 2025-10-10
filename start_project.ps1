# AI Car Marketplace - Enhanced Edition Startup Script
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  AI Car Marketplace - Enhanced Edition" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""

# Function to check if a port is in use
function Test-Port {
    param([int]$Port)
    try {
        $connection = New-Object System.Net.Sockets.TcpClient
        $connection.Connect("localhost", $Port)
        $connection.Close()
        return $true
    }
    catch {
        return $false
    }
}

# Check Python dependencies
Write-Host "[1/4] Checking Python dependencies..." -ForegroundColor Yellow
try {
    python -c "import flask, pandas, sklearn; print('✓ Python dependencies OK')" 2>$null
    Write-Host "✓ Python dependencies OK" -ForegroundColor Green
}
catch {
    Write-Host "✗ Missing Python dependencies. Installing..." -ForegroundColor Red
    pip install -r requirements.txt
}

Write-Host ""

# Check Node.js dependencies
Write-Host "[2/4] Checking Node.js dependencies..." -ForegroundColor Yellow
Set-Location client
if (-not (Test-Path "node_modules")) {
    Write-Host "✗ Node modules missing. Installing..." -ForegroundColor Red
    npm install
} else {
    Write-Host "✓ Node modules OK" -ForegroundColor Green
}

Write-Host ""

# Start Flask Backend
Write-Host "[3/4] Starting Flask Backend Server..." -ForegroundColor Yellow
Set-Location ..
if (Test-Port 5000) {
    Write-Host "⚠ Port 5000 is already in use. Flask server may already be running." -ForegroundColor Yellow
} else {
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "python unified_app.py" -WindowStyle Normal
    Write-Host "✓ Flask Backend starting..." -ForegroundColor Green
}

Write-Host ""

# Start React Frontend
Write-Host "[4/4] Starting React Frontend Server..." -ForegroundColor Yellow
Set-Location client
if (Test-Port 3000) {
    Write-Host "⚠ Port 3000 is already in use. React server may already be running." -ForegroundColor Yellow
} else {
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "npm start" -WindowStyle Normal
    Write-Host "✓ React Frontend starting..." -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Servers Starting..." -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "✓ Flask Backend: http://localhost:5000" -ForegroundColor Cyan
Write-Host "✓ React Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Write-Host "✓ Market Trends: http://localhost:3000/market-trends" -ForegroundColor Cyan
Write-Host "✓ Dashboard: http://localhost:3000/dashboard" -ForegroundColor Cyan
Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "  Development Login Credentials:" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "✓ Email: any@example.com" -ForegroundColor White
Write-Host "✓ OTP: any 6-digit number" -ForegroundColor White
Write-Host ""
Write-Host "Press any key to close this window..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
