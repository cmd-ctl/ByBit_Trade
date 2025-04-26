# Bybit Spot Trading Snipe Bot - Documentation

## Overview
This Python script provides automated spot trading functionality on Bybit exchange with:
- Scheduled trading execution
- Market buy orders
- Limit sell orders
- Price monitoring
- Balance checking
- Comprehensive logging

## Requirements
- Python 3.8+
- Required packages:
  - `pybit` (Bybit API wrapper)
  - `python-dotenv`
  - `logging`
  - `past` (for Python 2/3 compatibility)

## Installation
1. Clone the repository or download both files (`snipe.py` and `balance.py`)
2. Install dependencies:
```bash
pip install pybit python-dotenv logging past
```

## Configuration

### Environment Variables
Create a `.env` file with your configuration:
```env
API_KEY=your_bybit_api_key
SECRET=your_bybit_api_secret
TICKER=BTCUSDT  # Trading pair
ROUND_QUANTITY=0.001  # Minimum trade quantity step
```

### File Structure
- `snipe.py` - Main trading script
- `balance.py` - Balance checking module
- `snipe_system.log` - Generated log file
- `.env` - Configuration file (not included in repo)

## Main Features

### 1. Scheduled Trading
- Executes trades at precisely specified times
- Countdown timer shows remaining time
- Supports both testnet and mainnet

### 2. Trading Logic
- Places market buy orders when conditions are met
- Automatically calculates sell quantity
- Places limit sell orders at user-specified price

### 3. Price Monitoring
- Real-time bid/ask price display
- Stop-buy price protection
- Continuous price checking

### 4. Balance Tracking
- Displays current wallet balances
- Shows available amounts for trading
- Integrated with main trading flow

## Usage

### Running the Script
```bash
python snipe.py
```

### Interactive Configuration
When running, the script will prompt for:
1. Sell limit-order price
2. Trade amount in base token
3. Stop-buy price (maximum buy price)
4. Execution time (YYYY, MM, DD, HH, MM format)

### Example Session
```
Starting program...
Notice: only for SPOT trading

--- BTCUSDT ---
Current prices:
BidPrice: 42500.50
AskPrice: 42501.00
---

Set sell limit-order price:
43000
Set the Amount (in basic token):
100
Set Stop-buy price:
42800

Enter the time to start:
(YYYY, MM, DD, HH, MM)
2023, 12, 15, 14, 30
Time remaining: 0:05:23
...
```

## Functions

### `snipe.py` Functions
- `connect()` - Establishes Bybit API connection
- `chk_price()` - Checks current market prices
- `main()` - Main execution loop with trading logic

### `balance.py` Functions
- `chk_balance()` - Retrieves and displays wallet balances

## Error Handling
- Comprehensive logging to `snipe_system.log`
- API error catching and display
- Price validation checks
- Connection error handling

## Security Notes
- Never share your `.env` file
- Use API keys with appropriate permissions only
- Consider using testnet for development
- The script only requires trading permissions

## Customization
1. Change rounding precision via `ROUND_QUANTITY`
2. Modify logging format in `logging.basicConfig`
3. Adjust sleep interval in main loop
4. Add additional order types as needed

## Output Example
```
 >> Buy order successful 

Current wallet balance:
---
Coin: BTC -> 0.0235
Coin: USDT -> 1250.50
---

BTCUSDT amount for sell: 0.023
 >> Sell Limit-order placed 
<Press -Enter- for exit>
```


## ⚠️ Known issues to be fixed: </br>
- not correct count of sell amount
