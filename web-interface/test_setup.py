#!/usr/bin/env python3
"""
HPTA Web Interface Setup Test
Tests the basic functionality of the web interface components
"""

import requests
import json
import time
import sys

def test_cli_server():
    """Test if CLI server is running"""
    try:
        response = requests.post('http://localhost:5001/run', 
                               json={'command': 'echo "test"'},
                               timeout=5)
        if response.status_code == 200:
            print("✅ CLI Server is running")
            return True
        else:
            print(f"❌ CLI Server returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ CLI Server is not accessible: {e}")
        return False

def test_web_interface():
    """Test if web interface is running"""
    try:
        response = requests.get('http://localhost:3000/', timeout=5)
        if response.status_code == 200:
            print("✅ Web Interface is running")
            return True
        else:
            print(f"❌ Web Interface returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Web Interface is not accessible: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints"""
    try:
        # Test key status endpoint
        response = requests.get('http://localhost:3000/api/keyStatus', timeout=5)
        if response.status_code == 200:
            print("✅ API endpoints are accessible")
            return True
        else:
            print(f"❌ API endpoints returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ API endpoints are not accessible: {e}")
        return False

def main():
    print("🧪 Testing HPTA Web Interface Setup...")
    print("=" * 50)
    
    tests = [
        ("CLI Server", test_cli_server),
        ("Web Interface", test_web_interface),
        ("API Endpoints", test_api_endpoints)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Testing {test_name}...")
        if test_func():
            passed += 1
        time.sleep(1)
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! HPTA Web Interface is ready to use.")
        print("\n📋 Next steps:")
        print("1. Open http://localhost:3000 in your browser")
        print("2. Enter your Gemini API keys")
        print("3. Start using the interface!")
        return 0
    else:
        print("❌ Some tests failed. Please check the setup.")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure Docker is running")
        print("2. Run: docker-compose up --build")
        print("3. Check logs: docker-compose logs")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 