import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv('BINGX_BASE_URL')

class PriceFetcher:
    def __init__(self):
        self.base_url = BASE_URL
    
    def get_current_price(self, symbol):
        """Get current market price for a symbol"""
        try:
            endpoint = f"{self.base_url}/openApi/swap/v2/quote/price"
            params = {'symbol': symbol}
            response = requests.get(endpoint, params=params)
            if response.status_code == 200:
                data = response.json()
                if data['code'] == 0:
                    price = float(data['data']['price'])
                    return price
                else:
                    print(f"Error: {data}")
                    return None
            else:
                print(f"HTTP Error: {response.status_code}")
                return None
        except Exception as e:
            print(f"Exception: {e}")
            return None
    
    def get_ticker_info(self, symbol):
        """Get detailed ticker information"""
        try:
            endpoint = f"{self.base_url}/openApi/swap/v2/quote/ticker"
            params = {'symbol': symbol}
            response = requests.get(endpoint, params=params)
            if response.status_code == 200:
                data = response.json()
                if data['code'] == 0:
                    return data['data']
                else:
                    print(f"Error: {data}")
                    return None
            else:
                print(f"HTTP Error: {response.status_code}")
                return None
        except Exception as e:
            print(f"Exception: {e}")
            return None
    
    def get_available_symbols(self):
        """Get list of available trading symbols"""
        try:
            endpoint = f"{self.base_url}/openApi/swap/v2/quote/contracts"
            response = requests.get(endpoint)
            if response.status_code == 200:
                data = response.json()
                if data['code'] == 0:
                    symbols = [contract['symbol'] for contract in data['data']]
                    return symbols
                else:
                    print(f"Error: {data}")
                    return None
            else:
                print(f"HTTP Error: {response.status_code}")
                return None
        except Exception as e:
            print(f"Exception: {e}")
            return None

def test_price_fetcher():
    """Test the price fetcher"""
    print("=" * 60)
    print("Testing Price Fetcher")
    print("=" * 60)
    
    fetcher = PriceFetcher()
    
    # Test with BTC-USDT
    symbol = "BTC-USDT"
    print(f"\n[Test 1] Getting current price for {symbol}...")
    price = fetcher.get_current_price(symbol)
    if price:
        print(f"✅ Current {symbol} Price: ${price:,.2f}")
    else:
        print(f"❌ Failed to get price")
    
    print(f"\n[Test 2] Getting ticker info for {symbol}...")
    ticker = fetcher.get_ticker_info(symbol)
    if ticker:
        print(f"✅ Ticker Info:")
        print(f"   Last Price: ${float(ticker['lastPrice']):,.2f}")
        print(f"   24h High: ${float(ticker['highPrice']):,.2f}")
        print(f"   24h Low: ${float(ticker['lowPrice']):,.2f}")
        print(f"   24h Volume: {float(ticker['volume']):,.2f}")
    else:
        print(f"❌ Failed to get ticker info")
    
    print(f"\n[Test 3] Getting available symbols...")
    symbols = fetcher.get_available_symbols()
    if symbols:
        print(f"✅ Found {len(symbols)} trading pairs")
        print(f"   First 10 symbols: {symbols[:10]}")
    else:
        print(f"❌ Failed to get symbols")
    
    print("\n" + "=" * 60)
    print("✅ Price Fetcher Tests Complete!")
    print("=" * 60)

if __name__ == "__main__":
    test_price_fetcher()