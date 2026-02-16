import os
import time
import hmac
import hashlib
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

API_KEY = os.getenv('BINGX_API_KEY')
SECRET_KEY = os.getenv('BINGX_SECRET_KEY')
BASE_URL = os.getenv('BINGX_BASE_URL')

def generate_signature(params, secret_key):
    """Generate signature for BingX API"""
    query_string = '&'.join([f"{key}={params[key]}" for key in sorted(params.keys())])
    signature = hmac.new(secret_key.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
    return signature

def test_connection():
    """Test connection to BingX API"""
    print("=" * 50)
    print("Testing BingX API Connection...")
    print("=" * 50)
    
    # Test 1: Get server time (no authentication needed)
    print("\n[Test 1] Getting server time...")
    try:
        response = requests.get(f"{BASE_URL}/openApi/swap/v2/server/time")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Server time: {data}")
        else:
            print(f"❌ Failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test 2: Get account balance (requires authentication)
    print("\n[Test 2] Getting account balance...")
    try:
        timestamp = int(time.time() * 1000)
        params = {
            'timestamp': timestamp
        }
        
        signature = generate_signature(params, SECRET_KEY)
        params['signature'] = signature
        
        headers = {
            'X-BX-APIKEY': API_KEY
        }
        
        response = requests.get(f"{BASE_URL}/openApi/swap/v2/user/balance", params=params, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Authentication Successful!")
            print(f"Response: {data}")
        else:
            print(f"❌ Failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("✅ ALL TESTS PASSED! API Connection Working!")
    print("=" * 50)
    return True

if __name__ == "__main__":
    test_connection()