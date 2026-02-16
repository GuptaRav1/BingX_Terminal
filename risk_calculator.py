class RiskCalculator:
    def __init__(self, fixed_risk_usd=5.0):
        """Initialize risk calculator with fixed dollar risk"""
        self.fixed_risk_usd = fixed_risk_usd
    
    def calculate_position_size(self, entry_price, stop_loss_price, leverage=1):
        """Calculate position size based on risk and stop loss distance"""
        try:
            # Calculate the distance between entry and stop loss
            stop_distance = abs(entry_price - stop_loss_price)
            
            # Determine direction
            if stop_loss_price < entry_price:
                direction = "LONG"
            elif stop_loss_price > entry_price:
                direction = "SHORT"
            else:
                return None, "Error: Stop loss cannot equal entry price"
            
            # Calculate risk percentage
            risk_percentage = (stop_distance / entry_price) * 100
            
            # Calculate position size in USD
            # Position Size = Risk Amount / (Distance in %)
            position_size_usd = self.fixed_risk_usd / (risk_percentage / 100)
            
            # Apply leverage
            position_size_usd = position_size_usd * leverage
            
            # Calculate quantity (contracts)
            quantity = position_size_usd / entry_price
            
            # Calculate potential profit if TP is 2x the risk distance
            take_profit_distance = stop_distance * 2
            if direction == "LONG":
                take_profit_price = entry_price + take_profit_distance
            else:
                take_profit_price = entry_price - take_profit_distance
            
            potential_profit = self.fixed_risk_usd * 2  # 2:1 Risk-Reward
            
            result = {
                'direction': direction,
                'entry_price': entry_price,
                'stop_loss_price': stop_loss_price,
                'take_profit_price': take_profit_price,
                'stop_distance': stop_distance,
                'risk_percentage': risk_percentage,
                'position_size_usd': position_size_usd,
                'quantity': quantity,
                'fixed_risk_usd': self.fixed_risk_usd,
                'potential_profit_usd': potential_profit,
                'risk_reward_ratio': 2.0,
                'leverage': leverage
            }
            
            return result, None
            
        except Exception as e:
            return None, f"Calculation error: {str(e)}"
    
    def set_risk_amount(self, new_risk_usd):
        """Update the fixed risk amount"""
        self.fixed_risk_usd = new_risk_usd
    
    def format_result(self, result):
        """Format calculation result for display"""
        if result is None:
            return "No result to format"
        
        output = "\n" + "=" * 60 + "\n"
        output += "POSITION SIZE CALCULATION\n"
        output += "=" * 60 + "\n"
        output += f"Direction: {result['direction']}\n"
        output += f"Entry Price: ${result['entry_price']:,.2f}\n"
        output += f"Stop Loss: ${result['stop_loss_price']:,.2f}\n"
        output += f"Take Profit: ${result['take_profit_price']:,.2f}\n"
        output += "-" * 60 + "\n"
        output += f"Stop Distance: ${result['stop_distance']:,.2f} ({result['risk_percentage']:.2f}%)\n"
        output += f"Fixed Risk: ${result['fixed_risk_usd']:.2f}\n"
        output += f"Leverage: {result['leverage']}x\n"
        output += "-" * 60 + "\n"
        output += f"Position Size: ${result['position_size_usd']:,.2f}\n"
        output += f"Quantity: {result['quantity']:.4f} contracts\n"
        output += "-" * 60 + "\n"
        output += f"Risk-Reward Ratio: 1:{result['risk_reward_ratio']}\n"
        output += f"Potential Loss: -${result['fixed_risk_usd']:.2f}\n"
        output += f"Potential Profit: +${result['potential_profit_usd']:.2f}\n"
        output += "=" * 60 + "\n"
        
        return output

def test_risk_calculator():
    """Test the risk calculator with examples"""
    print("=" * 60)
    print("Testing Risk Calculator")
    print("=" * 60)
    
    calc = RiskCalculator(fixed_risk_usd=5.0)
    
    # Test 1: LONG position
    print("\n[Test 1] LONG Position Example")
    print("Scenario: BTC at $100,000, Stop Loss at $99,500")
    result, error = calc.calculate_position_size(
        entry_price=100000,
        stop_loss_price=99500,
        leverage=1
    )
    if result:
        print(calc.format_result(result))
    else:
        print(f"❌ Error: {error}")
    
    # Test 2: SHORT position
    print("\n[Test 2] SHORT Position Example")
    print("Scenario: BTC at $100,000, Stop Loss at $100,500")
    result, error = calc.calculate_position_size(
        entry_price=100000,
        stop_loss_price=100500,
        leverage=1
    )
    if result:
        print(calc.format_result(result))
    else:
        print(f"❌ Error: {error}")
    
    # Test 3: With leverage
    print("\n[Test 3] LONG Position with 5x Leverage")
    print("Scenario: BTC at $100,000, Stop Loss at $99,500, 5x Leverage")
    result, error = calc.calculate_position_size(
        entry_price=100000,
        stop_loss_price=99500,
        leverage=5
    )
    if result:
        print(calc.format_result(result))
    else:
        print(f"❌ Error: {error}")
    
    # Test 4: Smaller position (ETH example)
    print("\n[Test 4] LONG Position - ETH Example")
    print("Scenario: ETH at $3,500, Stop Loss at $3,450")
    result, error = calc.calculate_position_size(
        entry_price=3500,
        stop_loss_price=3450,
        leverage=1
    )
    if result:
        print(calc.format_result(result))
    else:
        print(f"❌ Error: {error}")
    
    print("\n" + "=" * 60)
    print("✅ Risk Calculator Tests Complete!")
    print("=" * 60)

if __name__ == "__main__":
    test_risk_calculator()