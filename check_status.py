#!/usr/bin/env python3
"""
AI Car Marketplace - Server Status Checker
"""

import requests
import time
import sys

def check_server(url, name, timeout=5):
    """Check if a server is running"""
    try:
        response = requests.get(url, timeout=timeout)
        return True, response.status_code
    except requests.exceptions.ConnectionError:
        return False, "Connection refused"
    except requests.exceptions.Timeout:
        return False, "Timeout"
    except Exception as e:
        return False, str(e)

def main():
    print("=" * 50)
    print("  AI Car Marketplace - Server Status")
    print("=" * 50)
    print()
    
    # Check Flask Backend
    print("Checking Flask Backend (Port 5000)...")
    flask_running, flask_status = check_server("http://localhost:5000", "Flask")
    if flask_running:
        print(f"✓ Flask Backend: RUNNING (Status: {flask_status})")
    else:
        print(f"✗ Flask Backend: NOT RUNNING ({flask_status})")
    
    print()
    
    # Check React Frontend (try both ports)
    print("Checking React Frontend (Ports 3000/3001)...")
    react_running, react_status = check_server("http://localhost:3000", "React")
    if not react_running:
        # Try port 3001 if 3000 is not available
        react_running, react_status = check_server("http://localhost:3001", "React")
    
    if react_running:
        print(f"✓ React Frontend: RUNNING (Status: {react_status})")
    else:
        print(f"✗ React Frontend: NOT RUNNING ({react_status})")
    
    print()
    print("=" * 50)
    
    if flask_running and react_running:
        print("🎉 Both servers are running!")
        print()
        print("Access URLs:")
        print("• Frontend: http://localhost:3000")
        print("• Backend:  http://localhost:5000")
        print("• Market Trends: http://localhost:3000/market-trends")
        print("• Dashboard: http://localhost:3000/dashboard")
        print()
        print("Development Login:")
        print("• Email: any@example.com")
        print("• OTP: any 6-digit number")
        return 0
    else:
        print("⚠️  Some servers are not running.")
        print()
        if not flask_running:
            print("To start Flask: python unified_app.py")
        if not react_running:
            print("To start React: cd client && npm start")
        print()
        print("Or use: .\\start_app.bat")
        return 1

if __name__ == "__main__":
    sys.exit(main())
