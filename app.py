from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from price_fetcher import PriceFetcher
from risk_calculator import RiskCalculator
from order_executor import OrderExecutor
import time
import requests

load_dotenv()

app = Flask(__name__)

# Initialize modules
price_fetcher = PriceFetcher()
risk_calculator = RiskCalculator(fixed_risk_usd=5.0)
order_executor = OrderExecutor()

# Global settings
current_symbol = "BTC-USDT"
current_risk = 5.0

@app.route('/')
def index():
    """Main trading terminal page"""
    return render_template('index.html')


@app.route('/chart')
def chart():
    """TradingView chart page"""
    return render_template('chart.html')

@app.route('/api/price/<symbol>')
def get_price(symbol):
    """Get current price for a symbol"""
    price = price_fetcher.get_current_price(symbol)
    if price:
        return jsonify({'success': True, 'price': price, 'symbol': symbol})
    else:
        return jsonify({'success': False, 'error': 'Failed to fetch price'})

@app.route('/api/ticker/<symbol>')
def get_ticker(symbol):
    """Get ticker info for a symbol"""
    ticker = price_fetcher.get_ticker_info(symbol)
    if ticker:
        return jsonify({'success': True, 'ticker': ticker})
    else:
        return jsonify({'success': False, 'error': 'Failed to fetch ticker'})

@app.route('/api/calculate', methods=['POST'])
def calculate_position():
    """Calculate position size based on risk parameters"""
    data = request.json
    entry_price = float(data.get('entry_price'))
    stop_loss_price = float(data.get('stop_loss_price'))
    leverage = int(data.get('leverage', 1))
    risk_amount = float(data.get('risk_amount', 5.0))
    risk_calculator.set_risk_amount(risk_amount)
    result, error = risk_calculator.calculate_position_size(entry_price, stop_loss_price, leverage)
    if result:
        return jsonify({'success': True, 'calculation': result})
    else:
        return jsonify({'success': False, 'error': error})

@app.route('/api/execute_trade', methods=['POST'])
def execute_trade():
    """Execute a market order with SL and TP"""
    data = request.json
    symbol = data.get('symbol')
    direction = data.get('direction')
    quantity = float(data.get('quantity'))
    stop_loss = float(data.get('stop_loss'))
    take_profit = float(data.get('take_profit'))
    side = 'BUY' if direction == 'LONG' else 'SELL'
    result, error = order_executor.place_market_order(symbol=symbol, side=side, quantity=quantity, stop_loss=stop_loss, take_profit=take_profit)
    if result:
        return jsonify({'success': True, 'order': result})
    else:
        return jsonify({'success': False, 'error': error})

@app.route('/api/balance')
def get_balance():
    """Get account balance"""
    balance, error = order_executor.get_account_balance()
    if balance:
        return jsonify({'success': True, 'balance': balance})
    else:
        return jsonify({'success': False, 'error': error})

@app.route('/api/positions')
def get_positions():
    """Get open positions"""
    positions, error = order_executor.get_open_positions()
    if positions:
        return jsonify({'success': True, 'positions': positions})
    else:
        return jsonify({'success': False, 'error': error})

@app.route('/api/symbols')
def get_symbols():
    """Get available trading symbols"""
    symbols = price_fetcher.get_available_symbols()
    if symbols:
        return jsonify({'success': True, 'symbols': symbols})
    else:
        return jsonify({'success': False, 'error': 'Failed to fetch symbols'})

@app.route('/api/set_risk', methods=['POST'])
def set_risk():
    """Update risk amount"""
    data = request.json
    new_risk = float(data.get('risk_amount', 5.0))
    risk_calculator.set_risk_amount(new_risk)
    return jsonify({'success': True, 'risk_amount': new_risk})


@app.route('/api/chart_data/<symbol>')
def get_chart_data(symbol):
    """Get candlestick data for chart"""
    try:
        endpoint = f"{BASE_URL}/openApi/swap/v2/quote/klines"
        params = {'symbol': symbol, 'interval': '15m', 'limit': 100}
        response = requests.get(endpoint, params=params)
        if response.status_code == 200:
            data = response.json()
            if data['code'] == 0:
                candles = [{'time': int(k['time'] / 1000), 'open': float(k['open']), 'high': float(k['high']), 'low': float(k['low']), 'close': float(k['close'])} for k in data['data']]
                return jsonify({'success': True, 'candles': candles})
        return jsonify({'success': False, 'error': 'Failed to fetch chart data'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 BingX Trading Terminal Starting...")
    print("=" * 60)
    print(f"Access your terminal at: http://localhost:5000")
    print("Press CTRL+C to stop the server")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)