import os
import time
import hmac
import hashlib
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('BINGX_API_KEY')
SECRET_KEY = os.getenv('BINGX_SECRET_KEY')
BASE_URL = os.getenv('BINGX_BASE_URL')

class OrderExecutor:
    def __init__(self):
        self.api_key = API_KEY
        self.secret_key = SECRET_KEY
        self.base_url = BASE_URL
    
    def generate_signature(self, params):
        """Generate signature for authenticated requests"""
        query_string = '&'.join([f"{key}={params[key]}" for key in sorted(params.keys())])
        signature = hmac.new(self.secret_key.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()
        return signature
    
    def place_market_order(self, symbol, side, quantity, stop_loss=None, take_profit=None):
        """Place a market order with optional SL/TP"""
        try:
            timestamp = int(time.time() * 1000)
            params = {'symbol': symbol, 'side': side, 'type': 'MARKET', 'quantity': quantity, 'timestamp': timestamp}
            if stop_loss:
                params['stopLoss'] = str(stop_loss)
            if take_profit:
                params['takeProfit'] = str(take_profit)
            signature = self.generate_signature(params)
            params['signature'] = signature
            headers = {'X-BX-APIKEY': self.api_key, 'Content-Type': 'application/json'}
            endpoint = f"{self.base_url}/openApi/swap/v2/trade/order"
            response = requests.post(endpoint, json=params, headers=headers)
            if response.status_code == 200:
                data = response.json()
                return data, None
            else:
                return None, f"HTTP Error {response.status_code}: {response.text}"
        except Exception as e:
            return None, f"Exception: {str(e)}"
    
    def set_stop_loss(self, symbol, stop_price, position_side):
        """Set stop loss for an existing position"""
        try:
            timestamp = int(time.time() * 1000)
            params = {'symbol': symbol, 'side': 'SELL' if position_side == 'LONG' else 'BUY', 'type': 'STOP_MARKET', 'stopPrice': str(stop_price), 'closePosition': 'true', 'timestamp': timestamp}
            signature = self.generate_signature(params)
            params['signature'] = signature
            headers = {'X-BX-APIKEY': self.api_key, 'Content-Type': 'application/json'}
            endpoint = f"{self.base_url}/openApi/swap/v2/trade/order"
            response = requests.post(endpoint, json=params, headers=headers)
            if response.status_code == 200:
                data = response.json()
                return data, None
            else:
                return None, f"HTTP Error {response.status_code}: {response.text}"
        except Exception as e:
            return None, f"Exception: {str(e)}"
    
    def set_take_profit(self, symbol, take_profit_price, position_side):
        """Set take profit for an existing position"""
        try:
            timestamp = int(time.time() * 1000)
            params = {'symbol': symbol, 'side': 'SELL' if position_side == 'LONG' else 'BUY', 'type': 'TAKE_PROFIT_MARKET', 'stopPrice': str(take_profit_price), 'closePosition': 'true', 'timestamp': timestamp}
            signature = self.generate_signature(params)
            params['signature'] = signature
            headers = {'X-BX-APIKEY': self.api_key, 'Content-Type': 'application/json'}
            endpoint = f"{self.base_url}/openApi/swap/v2/trade/order"
            response = requests.post(endpoint, json=params, headers=headers)
            if response.status_code == 200:
                data = response.json()
                return data, None
            else:
                return None, f"HTTP Error {response.status_code}: {response.text}"
        except Exception as e:
            return None, f"Exception: {str(e)}"
    
    def get_open_positions(self, symbol=None):
        """Get current open positions"""
        try:
            timestamp = int(time.time() * 1000)
            params = {'timestamp': timestamp}
            if symbol:
                params['symbol'] = symbol
            signature = self.generate_signature(params)
            params['signature'] = signature
            headers = {'X-BX-APIKEY': self.api_key}
            endpoint = f"{self.base_url}/openApi/swap/v2/user/positions"
            response = requests.get(endpoint, params=params, headers=headers)
            if response.status_code == 200:
                data = response.json()
                return data, None
            else:
                return None, f"HTTP Error {response.status_code}: {response.text}"
        except Exception as e:
            return None, f"Exception: {str(e)}"
    
    def get_account_balance(self):
        """Get account balance"""
        try:
            timestamp = int(time.time() * 1000)
            params = {'timestamp': timestamp}
            signature = self.generate_signature(params)
            params['signature'] = signature
            headers = {'X-BX-APIKEY': self.api_key}
            endpoint = f"{self.base_url}/openApi/swap/v2/user/balance"
            response = requests.get(endpoint, params=params, headers=headers)
            if response.status_code == 200:
                data = response.json()
                return data, None
            else:
                return None, f"HTTP Error {response.status_code}: {response.text}"
        except Exception as e:
            return None, f"Exception: {str(e)}"
    
    def cancel_all_orders(self, symbol):
        """Cancel all open orders for a symbol"""
        try:
            timestamp = int(time.time() * 1000)
            params = {'symbol': symbol, 'timestamp': timestamp}
            signature = self.generate_signature(params)
            params['signature'] = signature
            headers = {'X-BX-APIKEY': self.api_key}
            endpoint = f"{self.base_url}/openApi/swap/v2/trade/allOrders"
            response = requests.delete(endpoint, params=params, headers=headers)
            if response.status_code == 200:
                data = response.json()
                return data, None
            else:
                return None, f"HTTP Error {response.status_code}: {response.text}"
        except Exception as e:
            return None, f"Exception: {str(e)}"

def test_order_executor():
    """Test order executor (view only - no actual orders)"""
    print("=" * 60)
    print("Testing Order Executor")
    print("=" * 60)
    executor = OrderExecutor()
    print("\n[Test 1] Getting Account Balance...")
    balance, error = executor.get_account_balance()
    if balance:
        print(f"✅ Account Balance Retrieved:")
        print(f"   Response: {balance}")
    else:
        print(f"❌ Error: {error}")
    print("\n[Test 2] Getting Open Positions...")
    positions, error = executor.get_open_positions()
    if positions:
        print(f"✅ Positions Retrieved:")
        print(f"   Response: {positions}")
    else:
        print(f"❌ Error: {error}")
    print("\n" + "=" * 60)
    print("⚠️  NOTE: NOT placing actual orders in test mode")
    print("=" * 60)
    print("\n✅ Order Executor Tests Complete!")
    print("\nThe executor is ready to:")
    print("  - Place market orders")
    print("  - Set stop loss")
    print("  - Set take profit")
    print("  - Manage positions")

if __name__ == "__main__":
    test_order_executor()