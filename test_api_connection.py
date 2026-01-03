#!/usr/bin/env python3
"""
Test script to verify the validation API is running and accessible.
"""

import requests
import sys
from datetime import datetime

API_BASE_URL = "http://localhost:8001"

def test_api():
    """Test API connection and endpoints."""
    print("=" * 70)
    print("Testing Validation API Connection")
    print("=" * 70)
    
    # Test 1: Root endpoint
    print("\n1. Testing root endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/", timeout=3)
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ API is running: {data.get('message', 'Unknown')}")
            print(f"   ✓ Database status: {data.get('tinydb', 'Unknown')}")
        else:
            print(f"   ✗ API returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("   ✗ Cannot connect to API")
        print("   → Make sure the API server is running:")
        print("     python validation_api_tinydb.py")
        print("     OR")
        print("     python run_validator_tinydb.py")
        return False
    except requests.exceptions.Timeout:
        print("   ✗ Connection timeout")
        return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    # Test 2: Get validations endpoint
    print("\n2. Testing GET /api/validations...")
    try:
        response = requests.get(f"{API_BASE_URL}/api/validations", timeout=5)
        if response.status_code == 200:
            data = response.json()
            video_count = len(data.get('validations', {}))
            print(f"   ✓ Successfully retrieved validations")
            print(f"   ✓ Videos with validations: {video_count}")
        else:
            print(f"   ✗ Failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    # Test 3: POST validation endpoint
    print("\n3. Testing POST /api/validations...")
    try:
        test_validation = {
            "video_id": "TEST_VIDEO",
            "validation": {
                "timestamp": datetime.now().isoformat(),
                "status": "correct",
                "feedback": "Test validation from connection test",
                "validator": "test_script"
            }
        }
        response = requests.post(
            f"{API_BASE_URL}/api/validations",
            json=test_validation,
            timeout=5
        )
        if response.status_code == 200:
            result = response.json()
            print(f"   ✓ Successfully saved test validation")
            print(f"   ✓ Total validations for test video: {result.get('total_validations', 0)}")
            
            # Clean up test data
            print("\n4. Cleaning up test data...")
            delete_response = requests.delete(f"{API_BASE_URL}/api/validations/TEST_VIDEO", timeout=5)
            if delete_response.status_code == 200:
                print("   ✓ Test data cleaned up")
            else:
                print("   ⚠ Could not clean up test data (not critical)")
        else:
            print(f"   ✗ Failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False
    
    print("\n" + "=" * 70)
    print("✓ All API tests passed!")
    print("=" * 70)
    return True

if __name__ == "__main__":
    success = test_api()
    sys.exit(0 if success else 1)
