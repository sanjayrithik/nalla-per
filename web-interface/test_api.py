#!/usr/bin/env python3
"""
Test script to debug API key initialization
"""

import requests
import json

def test_api_key_init():
    """Test the API key initialization endpoint"""
    
    # Test with empty data
    print("Testing with empty data...")
    response = requests.post('http://localhost:3000/api/initKeys', 
                           json={})
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()
    
    # Test with empty keys array
    print("Testing with empty keys array...")
    response = requests.post('http://localhost:3000/api/initKeys', 
                           json={'keys': []})
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()
    
    # Test with None keys
    print("Testing with None keys...")
    response = requests.post('http://localhost:3000/api/initKeys', 
                           json={'keys': None})
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()
    
    # Test with empty string keys
    print("Testing with empty string keys...")
    response = requests.post('http://localhost:3000/api/initKeys', 
                           json={'keys': ['', '   ', '']})
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()
    
    # Test with invalid key format
    print("Testing with invalid key format...")
    response = requests.post('http://localhost:3000/api/initKeys', 
                           json={'keys': ['invalid_key']})
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print()

if __name__ == "__main__":
    test_api_key_init() 