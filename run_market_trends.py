#!/usr/bin/env python3
"""
Enhanced Car Price Predictor with Advanced Market Trends
Startup script for the complete application
"""

import os
import sys
import subprocess
import time
from datetime import datetime

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'flask', 'flask_cors', 'pandas', 'numpy', 'scikit-learn', 
        'scipy', 'pickle', 'warnings'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"   ✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"   ❌ {package} - Missing")
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("📦 Installing missing packages...")
        
        for package in missing_packages:
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
                print(f"   ✅ Installed {package}")
            except subprocess.CalledProcessError:
                print(f"   ❌ Failed to install {package}")
                return False
    
    return True

def check_data_files():
    """Check if required data files exist"""
    print("\n📁 Checking data files...")
    
    required_files = [
        'Cleaned_Car_data_master.csv',
        'LinearRegressionModel.pkl'
    ]
    
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"   ✅ {file} ({size:,} bytes)")
        else:
            missing_files.append(file)
            print(f"   ❌ {file} - Missing")
    
    if missing_files:
        print(f"\n⚠️  Missing required files: {', '.join(missing_files)}")
        print("Please ensure all data files are in the current directory.")
        return False
    
    return True

def test_market_analyzer():
    """Test the market trends analyzer"""
    print("\n🧪 Testing Market Trends Analyzer...")
    
    try:
        from market_trends_analyzer import MarketTrendsAnalyzer
        
        # Quick test
        analyzer = MarketTrendsAnalyzer()
        overview = analyzer.get_market_overview()
        
        print(f"   ✅ Analyzer working correctly")
        print(f"   📊 {overview['total_listings']:,} listings loaded")
        print(f"   💰 Average price: ₹{overview['average_price']:,.2f}")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Analyzer test failed: {str(e)}")
        return False

def create_directories():
    """Create necessary directories"""
    print("\n📂 Creating directories...")
    
    directories = ['static/css', 'templates', 'reports']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"   ✅ Created {directory}")
        else:
            print(f"   ✅ {directory} exists")

def display_banner():
    """Display application banner"""
    banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║    🚗 ADVANCED CAR PRICE PREDICTOR & MARKET TRENDS ANALYZER 🚗             ║
║                                                                              ║
║    Features:                                                                 ║
║    • 🎯 AI-Powered Price Prediction                                          ║
║    • 📊 Comprehensive Market Analysis                                        ║
║    • 📈 Real-time Trend Visualization                                        ║
║    • 🏢 Company Performance Comparison                                       ║
║    • 🔮 Market Predictions & Insights                                        ║
║    • 🌆 City-wise Market Analysis                                            ║
║    • ⛽ Fuel Type Distribution Analysis                                       ║
║    • 🧠 Advanced Analytics & Correlations                                    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def show_usage_instructions():
    """Show usage instructions"""
    instructions = """
🚀 APPLICATION READY!

📱 Access the application:
   • Main Application: http://localhost:5000
   • Market Trends: http://localhost:5000/market-trends

🔗 API Endpoints:
   • Market Overview: /api/market-overview
   • Company Trends: /api/company-trends  
   • Fuel Analysis: /api/fuel-type-analysis
   • City Analysis: /api/city-market-analysis
   • Price Trends: /api/price-trends
   • Market Predictions: /api/market-predictions
   • Advanced Analytics: /api/advanced-analytics
   • Comprehensive Report: /api/market-report

💡 Tips:
   • Use Ctrl+C to stop the server
   • Check the console for any errors
   • Refresh browser if charts don't load initially

🎯 Features Available:
   ✅ Price Prediction with ML Model
   ✅ Interactive Market Dashboards
   ✅ Real-time Data Visualization
   ✅ Advanced Market Analytics
   ✅ Company Performance Metrics
   ✅ Market Trend Predictions
   ✅ Export Capabilities (Coming Soon)
    """
    print(instructions)

def main():
    """Main startup function"""
    print("🚀 STARTING ENHANCED CAR PRICE PREDICTOR")
    print("=" * 80)
    print(f"⏰ Startup Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Display banner
    display_banner()
    
    # Step 1: Check dependencies
    if not check_dependencies():
        print("❌ Dependency check failed. Please install missing packages.")
        return False
    
    # Step 2: Check data files
    if not check_data_files():
        print("❌ Data file check failed. Please ensure all required files are present.")
        return False
    
    # Step 3: Create directories
    create_directories()
    
    # Step 4: Test market analyzer
    if not test_market_analyzer():
        print("❌ Market analyzer test failed.")
        return False
    
    print("\n✅ All checks passed! Starting application...")
    
    # Show usage instructions
    show_usage_instructions()
    
    # Start the Flask application
    try:
        print("\n🌐 Starting Flask server...")
        print("   📍 Server will start at: http://localhost:5000")
        print("   🔄 Loading... Please wait for 'Running on' message")
        print("\n" + "="*80)
        
        # Import and run the enhanced application
        from enhanced_application import app
        app.run(debug=True, host='0.0.0.0', port=5000)
        
    except KeyboardInterrupt:
        print("\n\n👋 Application stopped by user")
        return True
    except Exception as e:
        print(f"\n❌ Error starting application: {str(e)}")
        return False

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n✅ Application shutdown successfully")
        else:
            print("\n❌ Application encountered errors")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 Startup interrupted by user")
    except Exception as e:
        print(f"\n💥 Unexpected error: {str(e)}")
        sys.exit(1)
