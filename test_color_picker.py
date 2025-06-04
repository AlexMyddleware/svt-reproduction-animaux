#!/usr/bin/env python3
"""
Test script to verify the global color picker functionality works correctly.
"""

import requests
import json
import time
import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_color_picker_functionality():
    """Test the color picker functionality"""
    base_url = "http://localhost:5000"
    
    print("Testing Global Color Picker Functionality")
    print("=" * 50)
    
    # Test 1: Check if settings page loads
    try:
        response = requests.get(f"{base_url}/settings/", timeout=5)
        if response.status_code == 200:
            print("✓ Settings page loads successfully")
            if 'color-picker' in response.text:
                print("✓ Color picker element found in settings page")
            else:
                print("✗ Color picker element NOT found in settings page")
        else:
            print(f"✗ Settings page failed to load (status: {response.status_code})")
            return False
    except requests.exceptions.RequestException as e:
        print(f"✗ Could not connect to server: {e}")
        return False
    
    # Test 2: Get current font settings
    try:
        response = requests.get(f"{base_url}/settings/get-font", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"✓ Current font family: {data.get('font_family', 'Unknown')}")
                print(f"✓ Current font color: {data.get('font_color', 'Unknown')}")
            else:
                print("✗ Failed to get font settings")
        else:
            print(f"✗ Font settings endpoint failed (status: {response.status_code})")
    except requests.exceptions.RequestException as e:
        print(f"✗ Could not get font settings: {e}")
    
    # Test 3: Save new color settings
    test_colors = ["#ff0000", "#00ff00", "#0000ff", "#ffff00", "#ff00ff"]
    
    for color in test_colors:
        try:
            payload = {
                "auto_validate": True,
                "font_family": "Atkinson Hyperlegible",
                "font_color": color
            }
            response = requests.post(
                f"{base_url}/settings/save",
                json=payload,
                headers={'Content-Type': 'application/json'},
                timeout=5
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    print(f"✓ Successfully saved color {color}")
                else:
                    print(f"✗ Failed to save color {color}: {result.get('message', 'Unknown error')}")
            else:
                print(f"✗ Save failed for color {color} (status: {response.status_code})")
        except requests.exceptions.RequestException as e:
            print(f"✗ Could not save color {color}: {e}")
    
    # Test 4: Verify the saved color
    try:
        response = requests.get(f"{base_url}/settings/get-font", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                final_color = data.get('font_color')
                if final_color == test_colors[-1]:
                    print(f"✓ Color persistence verified: {final_color}")
                else:
                    print(f"✗ Color persistence failed. Expected: {test_colors[-1]}, Got: {final_color}")
            else:
                print("✗ Failed to verify saved color")
    except requests.exceptions.RequestException as e:
        print(f"✗ Could not verify saved color: {e}")
    
    # Test 5: Reset to default white
    try:
        payload = {
            "auto_validate": True,
            "font_family": "Atkinson Hyperlegible",
            "font_color": "#ffffff"
        }
        response = requests.post(
            f"{base_url}/settings/save",
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=5
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                print("✓ Reset to default white color successfully")
            else:
                print(f"✗ Failed to reset to default: {result.get('message', 'Unknown error')}")
    except requests.exceptions.RequestException as e:
        print(f"✗ Could not reset to default: {e}")
    
    print("\nTest completed! Check the browser to see the color changes in real-time.")
    print("Navigate to: http://localhost:5000/settings/")
    print("Try changing the color picker and watch all text change color!")
    
    return True

def test_different_pages():
    """Test color application on different pages"""
    base_url = "http://localhost:5000"
    pages_to_test = [
        "/",
        "/settings/",
        "/questions-tree/",
        "/texte-a-trous/",
        "/create-question/"
    ]
    
    print("\nTesting color application across different pages:")
    print("-" * 50)
    
    for page in pages_to_test:
        try:
            response = requests.get(f"{base_url}{page}", timeout=5)
            if response.status_code == 200:
                if 'font_manager.css' in response.text:
                    print(f"✓ {page} includes font manager CSS")
                else:
                    print(f"✗ {page} missing font manager CSS")
            else:
                print(f"✗ {page} failed to load (status: {response.status_code})")
        except requests.exceptions.RequestException as e:
            print(f"✗ {page} connection error: {e}")

if __name__ == "__main__":
    # Wait a moment for the server to start if it just started
    time.sleep(2)
    
    success = test_color_picker_functionality()
    if success:
        test_different_pages()
    
    print("\n" + "=" * 60)
    print("Global Color Picker Testing Complete!")
    print("=" * 60) 