#!/usr/bin/env python3
"""
Test script with real Gemini API keys
"""

import requests
import json

def test_real_keys():
    """Test with the real API keys provided"""
    
    real_keys = [
        "AIzaSyBVJvewTqG7wArWtczhsh95dxUHlHNVKW4",
        "AIzaSyDNrOXhxiaxtt3OJAB1R_0cPEnGF02eFu0", 
        "AIzaSyCqdY2TPZwo0vwtfXSD_-w6AU2BrF5NLWc"
    ]
    
    print("🧪 Testing Real Gemini API Keys...")
    print("=" * 50)
    
    for i, key in enumerate(real_keys, 1):
        print(f"\nTesting Key {i}: {key[:10]}...")
        
        response = requests.post('http://localhost:3000/api/initKeys', 
                               json={'keys': [key]})
        
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("✅ Key is working!")
        else:
            print("❌ Key validation failed")
    
    print("\n" + "=" * 50)
    print("Testing all keys together...")
    
    response = requests.post('http://localhost:3000/api/initKeys', 
                           json={'keys': real_keys})
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

if __name__ == "__main__":
    test_real_keys() 