# 🚀 Car Price Predictor - Complete Setup Guide

## 📋 Prerequisites

- **Python 3.8+** installed
- **Node.js 14+** and **npm 6+** installed
- **Git** (optional, for cloning)

## 🔧 Quick Setup (Recommended)

### Windows:
```bash
# Run the setup script
setup.bat
```

### Linux/Mac:
```bash
# Make script executable and run
chmod +x setup.sh
./setup.sh
```

## 🛠️ Manual Setup

### 1. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 2. Install Node.js Dependencies
```bash
# Install root dependencies
npm install

# Install React app dependencies
cd client
npm install
cd ..
```

### 3. Environment Configuration
```bash
# Create environment file for React
echo "REACT_APP_USE_LOCAL_AUTH=true" > client/.env
```

## 🚀 Running the Application

### Option 1: Use Startup Scripts (Easiest)

**Windows:**
```bash
start_app.bat
```

**Linux/Mac:**
```bash
chmod +x start_app.sh
./start_app.sh
```

### Option 2: Use npm Scripts
```bash
# Run both servers simultaneously
npm run run-all

# Or run separately:
npm run server    # Flask backend (port 5000)
npm run client    # React frontend (port 3000)
```

### Option 3: Manual Start
```bash
# Terminal 1: Flask Server
python unified_app.py

# Terminal 2: React App
cd client
npm start
```

## 🌐 Access the Application

- **React Frontend**: http://localhost:3000
- **Flask Backend**: http://localhost:5000
- **Market Trends**: http://localhost:3000/market-trends (after login)

## 🔑 Authentication

For development, use:
- **Email**: Any valid email format
- **OTP**: Any 6-digit number

## 📊 Features Available

### 🏠 Main Features:
- **Car Price Prediction**: ML-powered price estimation
- **User Authentication**: Secure login system
- **Dashboard**: Personal prediction history
- **Company Details**: Comprehensive car manufacturer info

### 📈 Market Trends (NEW):
- **Market Overview**: KPI cards with market statistics
- **Company Analysis**: Performance rankings and reliability scores
- **Fuel Type Analysis**: Distribution and trends by fuel type
- **City Market Analysis**: Geographic market insights
- **AI Predictions**: Trending companies and recommendations
- **Interactive Charts**: Beautiful visualizations with Chart.js

## 🔧 Troubleshooting

### Common Issues:

1. **"Module not found" errors**
   ```bash
   pip install -r requirements.txt
   cd client && npm install
   ```

2. **Port already in use**
   ```bash
   # Kill processes on ports 3000 and 5000
   npx kill-port 3000 5000
   ```

3. **React app can't connect to Flask**
   - Ensure Flask server is running on port 5000
   - Check proxy configuration in client/package.json

4. **Market Trends not loading**
   - Verify Flask server is running
   - Check browser console for errors
   - Ensure data files are present

### Data Files Required:
- `Cleaned_Car_data_master.csv` (main dataset)
- `BestCombinedModel.pkl` (ML model)
- `LinearRegressionModel.pkl` (backup model)

## 🚀 Deployment

### Heroku Deployment:
```bash
# The project is Heroku-ready with:
# - Procfile configured
# - heroku-postbuild script in package.json
# - Static file serving in unified_app.py

heroku create your-app-name
git push heroku main
```

### Local Production Build:
```bash
# Build React app
cd client
npm run build
cd ..

# Run with Gunicorn
gunicorn unified_app:app
```

## 📁 Project Structure

```
car_price_predictor/
├── unified_app.py              # Main Flask application
├── market_trends_analyzer.py   # Market analysis engine
├── requirements.txt            # Python dependencies
├── package.json               # Root npm configuration
├── Procfile                   # Heroku deployment
├── client/                    # React frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── MarketTrends.js # Market trends dashboard
│   │   │   └── ...
│   │   └── ...
│   └── package.json
├── static/                    # Static assets
├── templates/                 # Flask templates
├── data/                      # CSV datasets
├── models/                    # ML model files
└── scripts/                   # Utility scripts
```

## 🆘 Support

If you encounter any issues:

1. Check this guide first
2. Verify all dependencies are installed
3. Ensure data files are present
4. Check console logs for specific errors
5. Try the troubleshooting steps above

## 🎉 Success!

Once everything is running, you should see:
- ✅ Flask server on port 5000
- ✅ React app on port 3000
- ✅ Market trends dashboard accessible after login
- ✅ All features working seamlessly

Enjoy your advanced car price prediction system with market intelligence! 🚗📊
