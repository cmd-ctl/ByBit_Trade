## Bybit Spot Trading Snipe Bot

A Python bot for **automated, scheduled spot trading** on the Bybit exchange. Designed for traders who want to execute precise buy/sell operations at target times with minimal latency and full control over logic.

---

## Features

- Time-based trading: execute a market order at a specific future time
- Market buy + limit sell logic
- Live price monitoring
- Post-trade balance tracking (token + USDT)
- Configurable via `.env` file
- Simple & local (no database needed)
- Suitable for scalping/sniping strategies

---

## Requirements

- Python 3.8+
- Required packages:

```bash
pip install pybit python-dotenv
````

---

## Configuration

### `.env` file

Create a file `.env` in the project root:

```env
BYBIT_API_KEY=your_api_key
BYBIT_SECRET=your_secret
ROUND_QUANTITY=0.001          # Round precision for base token (e.g., TON)
TAKER_FEE_RATE=0.0006         # Optional: fee for accurate post-trade qty (default: 0.06%)
```

---

## File Structure

```
.
├── snipe.py           # Main trading script
├── .env               # API credentials and settings (not committed)
```

---

## How It Works

1. You input:

   * Trading pair (e.g., TONUSDT)
   * Amount in USDT
   * Target profit in %
   * Max entry price (optional)
   * Trigger time (UTC)

2. Script:

   * Waits for the exact time
   * Executes a **market buy**
   * Fetches **actual executed quantity**
   * Adjusts for **taker fee**
   * Rounds down to match Bybit’s lot step
   * Places a **limit sell order** at your target price
   * Shows updated balances (token + USDT)

---

## Example Session

```
Enter token pair (e.g., TONUSDT): TONUSDT
Enter amount in USDT: 100
Desired profit %: 2
Max entry price (0 for any): 0
Enter trigger time (YYYY, MM, DD, HH, MM): 2025, 05, 21, 14, 30
[INFO] Waiting until: 2025-05-21 14:30:00 UTC

[INFO] Time reached. Proceeding.
[INFO] Placing MARKET BUY for 100.0 USDT of TONUSDT
[SUCCESS] Buy order placed.

[INFO] Placing LIMIT SELL for 97.202 TON at 2.100000 USDT
[SUCCESS] Sell order placed. ID: 1234567890

After trade balances:
→ TON: 97.202
→ USDT: 1.23
```

---

## Functions Summary

### `snipe.py`

| Function             | Description                                |
| -------------------- | ------------------------------------------ |
| `wait_until()`       | Waits until specified UTC time             |
| `get_price()`        | Fetches current spot price from Bybit      |
| `place_market_buy()` | Places a market buy order for USDT amount  |
| `get_executed_qty()` | Retrieves filled amount (from actual buy)  |
| `round_down()`       | Rounds quantity to Bybit step              |
| `place_limit_sell()` | Places a limit sell order for bought token |
| `main()`             | Full execution flow                        |

---

## Known Limitations

* Works only for **SPOT** pairs (e.g., `TONUSDT`)
* No built-in Telegram alerts (can be added)
* Assumes sufficient USDT balance
* Slippage possible if market is thin

---

## License

MIT License – use at your own risk.

