#!/usr/bin/env python3
"""
Debug script to test API key initialization with sample data
"""

import requests
import json

def test_with_sample_key():
    """Test with a sample API key format"""
    
    # Test with a sample key (this is not a real key, just for format testing)
    sample_key = "AIzaSyC" + "x" * 35  # Simulate a Gemini API key format
    
    print("Testing with sample key format...")
    print(f"Sample key: {sample_key[:10]}...")
    
    response = requests.post('http://localhost:3000/api/initKeys', 
                           json={'keys': [sample_key]})
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_with_real_key_format():
    """Test with what a real Gemini key should look like"""
    
    # Real Gemini API keys typically start with "AIza" and are about 39 characters
    real_format_key = "AIzaSyC" + "x" * 33  # 39 characters total
    
    print("Testing with real key format...")
    print(f"Key length: {len(real_format_key)}")
    print(f"Key format: {real_format_key[:10]}...")
    
    response = requests.post('http://localhost:3000/api/initKeys', 
                           json={'keys': [real_format_key]})
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

def test_key_validation():
    """Test the key validation logic"""
    
    # Test various key formats
    test_keys = [
        "",  # Empty
        "   ",  # Whitespace only
        "short",  # Too short
        "AIzaSyC" + "x" * 33,  # Correct format but invalid
        "AIzaSyC" + "x" * 35,  # Too long
    ]
    
    for i, key in enumerate(test_keys):
        print(f"Test {i+1}: Key = '{key[:10]}{'...' if len(key) > 10 else ''}' (length: {len(key)})")
        
        response = requests.post('http://localhost:3000/api/initKeys', 
                               json={'keys': [key]})
        
        print(f"  Status: {response.status_code}")
        print(f"  Response: {response.json()}")
        print()

if __name__ == "__main__":
    print("🧪 Debugging API Key Issues...")
    print("=" * 50)
    
    test_with_sample_key()
    test_with_real_key_format()
    test_key_validation() 