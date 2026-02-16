import requests
from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = os.getenv('BINGX_BASE_URL')

def test_chart_data():
    """Test getting chart data from BingX"""
    print("=" * 60)
    print("Testing Chart Data API")
    print("=" * 60)
    
    symbol = "BTC-USDT"
    
    print(f"\n[Test] Getting candlestick data for {symbol}...")
    
    endpoint = f"{BASE_URL}/openApi/swap/v2/quote/klines"
    params = {
        'symbol': symbol,
        'interval': '15m',
        'limit': 100
    }
    
    try:
        response = requests.get(endpoint, params=params)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:500]}")  # First 500 chars
        
        if response.status_code == 200:
            data = response.json()
            print(f"\nFull response structure: {data}")
            
            if data.get('code') == 0:
                print(f"\n✅ Success! Got {len(data['data'])} candles")
                print(f"First candle: {data['data'][0]}")
                print(f"Last candle: {data['data'][-1]}")
            else:
                print(f"\n❌ API returned error code: {data.get('code')}")
                print(f"Message: {data.get('msg')}")
        else:
            print(f"\n❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"\n❌ Exception: {e}")

if __name__ == "__main__":
    test_chart_data()