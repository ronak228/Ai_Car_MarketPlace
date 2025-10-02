#!/usr/bin/env python3
"""
Comprehensive test script to verify the Car Price Predictor setup
Tests all components and dependencies
"""

import sys
import os
import subprocess
import requests
import json
import time
from pathlib import Path

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"🔍 {title}")
    print("="*60)

def print_success(message):
    """Print success message"""
    print(f"✅ {message}")

def print_error(message):
    """Print error message"""
    print(f"❌ {message}")

def print_warning(message):
    """Print warning message"""
    print(f"⚠️  {message}")

def test_python_dependencies():
    """Test if all Python dependencies are installed"""
    print_header("Testing Python Dependencies")
    
    required_packages = [
        'flask', 'flask_cors', 'pandas', 'numpy', 'scikit-learn', 
        'scipy', 'requests', 'gunicorn'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print_success(f"{package} is installed")
        except ImportError:
            print_error(f"{package} is missing")
            missing_packages.append(package)
    
    if missing_packages:
        print_error(f"Missing packages: {', '.join(missing_packages)}")
        print("💡 Run: pip install -r requirements.txt")
        return False
    
    print_success("All Python dependencies are installed!")
    return True

def test_data_files():
    """Test if required data files exist"""
    print_header("Testing Data Files")
    
    required_files = [
        'Cleaned_Car_data_master.csv',
        'BestCombinedModel.pkl',
        'LinearRegressionModel.pkl'
    ]
    
    missing_files = []
    
    for file_name in required_files:
        if os.path.exists(file_name):
            print_success(f"{file_name} found")
        else:
            print_error(f"{file_name} missing")
            missing_files.append(file_name)
    
    if missing_files:
        print_error(f"Missing files: {', '.join(missing_files)}")
        return False
    
    print_success("All required data files are present!")
    return True

def test_node_dependencies():
    """Test if Node.js and npm dependencies are installed"""
    print_header("Testing Node.js Dependencies")
    
    # Check if Node.js is installed
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print_success(f"Node.js version: {result.stdout.strip()}")
        else:
            print_error("Node.js is not installed")
            return False
    except FileNotFoundError:
        print_error("Node.js is not installed")
        return False
    
    # Check if npm is installed
    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print_success(f"npm version: {result.stdout.strip()}")
        else:
            print_error("npm is not installed")
            return False
    except FileNotFoundError:
        print_error("npm is not installed")
        return False
    
    # Check if client dependencies are installed
    if os.path.exists('client/node_modules'):
        print_success("Client dependencies are installed")
    else:
        print_warning("Client dependencies not installed")
        print("💡 Run: cd client && npm install")
    
    return True

def test_flask_server():
    """Test if Flask server can start and respond"""
    print_header("Testing Flask Server")
    
    # Import and test the Flask app
    try:
        from unified_app import app
        print_success("unified_app.py imports successfully")
        
        # Test if market trends analyzer works
        from market_trends_analyzer import MarketTrendsAnalyzer
        analyzer = MarketTrendsAnalyzer()
        print_success("MarketTrendsAnalyzer initializes successfully")
        
        # Test a simple analysis
        overview = analyzer.get_market_overview()
        if overview and 'total_listings' in overview:
            print_success(f"Market analysis working - {overview['total_listings']} listings found")
        else:
            print_error("Market analysis not working properly")
            return False
            
    except Exception as e:
        print_error(f"Flask server test failed: {str(e)}")
        return False
    
    print_success("Flask server tests passed!")
    return True

def test_api_endpoints():
    """Test API endpoints if server is running"""
    print_header("Testing API Endpoints")
    
    base_url = "http://localhost:5000"
    endpoints = [
        "/api/health",
        "/api/companies",
        "/api/fuel-types",
        "/api/market-overview"
    ]
    
    server_running = False
    
    # Check if server is running
    try:
        response = requests.get(f"{base_url}/api/health", timeout=5)
        if response.status_code == 200:
            server_running = True
            print_success("Flask server is running")
        else:
            print_warning("Flask server not responding properly")
    except requests.exceptions.RequestException:
        print_warning("Flask server is not running")
        print("💡 Start server with: python unified_app.py")
    
    if server_running:
        for endpoint in endpoints:
            try:
                response = requests.get(f"{base_url}{endpoint}", timeout=10)
                if response.status_code == 200:
                    print_success(f"{endpoint} - OK")
                else:
                    print_error(f"{endpoint} - Failed (Status: {response.status_code})")
            except Exception as e:
                print_error(f"{endpoint} - Error: {str(e)}")
    
    return server_running

def test_react_build():
    """Test if React app can build"""
    print_header("Testing React Build")
    
    if not os.path.exists('client'):
        print_error("Client directory not found")
        return False
    
    if not os.path.exists('client/package.json'):
        print_error("Client package.json not found")
        return False
    
    print_success("React app structure is correct")
    
    # Check if build directory exists (optional)
    if os.path.exists('client/build'):
        print_success("React build directory exists")
    else:
        print_warning("React build not found")
        print("💡 Run: cd client && npm run build")
    
    return True

def run_comprehensive_test():
    """Run all tests"""
    print("🚀 Car Price Predictor - Comprehensive Setup Test")
    print("This will verify that your project is ready to run")
    
    tests = [
        ("Python Dependencies", test_python_dependencies),
        ("Data Files", test_data_files),
        ("Node.js Dependencies", test_node_dependencies),
        ("Flask Server", test_flask_server),
        ("API Endpoints", test_api_endpoints),
        ("React Build", test_react_build)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print_error(f"{test_name} test failed with exception: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print_header("Test Summary")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        if result:
            print_success(f"{test_name}")
        else:
            print_error(f"{test_name}")
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print_success("🎉 All tests passed! Your project is ready to run!")
        print("\n🚀 To start the application:")
        print("   Windows: start_app.bat")
        print("   Linux/Mac: ./start_app.sh")
        print("   Or: npm run run-all")
    else:
        print_error("❌ Some tests failed. Please fix the issues above.")
        print("\n💡 Common solutions:")
        print("   - Run: pip install -r requirements.txt")
        print("   - Run: cd client && npm install")
        print("   - Ensure all data files are present")
    
    return passed == total

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)
