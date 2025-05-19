import os
import time
import math
import datetime
from dotenv import load_dotenv
from pybit.unified_trading import HTTP

load_dotenv()

API_KEY = os.environ["BYBIT_API_KEY"]
API_SECRET = os.environ["BYBIT_SECRET"]
ROUND_QUANTITY = float(os.environ.get("ROUND_QUANTITY", 0.0001))
TAKER_FEE_RATE = float(os.environ.get("TAKER_FEE_RATE", 0.0006))  # Default 0.06%

client = HTTP(
    api_key=API_KEY,
    api_secret=API_SECRET
)

def wait_until(start_time):
    print(f"[INFO] Waiting until: {start_time.strftime('%Y-%m-%d %H:%M:%S')} UTC")
    while datetime.datetime.utcnow() < start_time:
        time.sleep(0.1)
    print("[INFO] Time reached. Proceeding.")

def get_price(symbol):
    try:
        res = client.get_tickers(category="spot", symbol=symbol)
        return float(res["result"]["list"][0]["lastPrice"])
    except Exception as e:
        print(f"[ERROR] Failed to fetch price: {e}")
        return 0.0

def place_market_buy(symbol, usdt_amount):
    print(f"[INFO] Placing MARKET BUY for {usdt_amount} USDT of {symbol}")
    try:
        order = client.place_order(
            category="spot",
            symbol=symbol,
            side="Buy",
            orderType="Market",
            quoteQty=round(usdt_amount, 2)
        )
        return order["result"]["orderId"]
    except Exception as e:
        print(f"[ERROR] Failed to place BUY order: {e}")
        return None

def get_executed_qty(order_id):
    try:
        time.sleep(0.3)
        data = client.get_order_history(category="spot", orderId=order_id)
        return float(data["result"]["list"][0]["cumExecQty"])
    except Exception as e:
        print(f"[ERROR] Failed to fetch executed quantity: {e}")
        return 0.0

def round_down(value, step):
    return math.floor(value / step) * step

def place_limit_sell(symbol, qty, price):
    print(f"[INFO] Placing LIMIT SELL for {qty} {symbol} at {price} USDT")
    try:
        order = client.place_order(
            category="spot",
            symbol=symbol,
            side="Sell",
            orderType="Limit",
            qty=qty,
            price=price,
            timeInForce="GTC"
        )
        return order["result"]["orderId"]
    except Exception as e:
        print(f"[ERROR] Failed to place SELL order: {e}")
        return None

def main():
    # --- Input ---
    pair = input("Enter token pair (e.g., TONUSDT): ").upper()
    amount_usdt = float(input("Enter amount in USDT: "))
    profit_percent = float(input("Desired profit %: "))
    entry_price_limit = float(input("Max entry price (0 for any): "))
    t_str = input("Enter trigger time (YYYY, MM, DD, HH, MM): ")

    trigger_time = datetime.datetime.strptime(t_str, '%Y, %m, %d, %H, %M')
    wait_until(trigger_time)

    # --- Price Check ---
    market_price = get_price(pair)
    if market_price == 0 or (entry_price_limit > 0 and market_price > entry_price_limit):
        print("[WARN] Market price too high or unavailable. Exiting.")
        return

    # --- Market Buy ---
    order_id = place_market_buy(pair, amount_usdt)
    if not order_id:
        return

    # --- Get Executed Qty ---
    exec_qty = get_executed_qty(order_id)
    if exec_qty == 0:
        print("[ERROR] Executed quantity is zero. Aborting.")
        return

    # --- Adjust for Fee and Round ---
    exec_qty *= (1 - TAKER_FEE_RATE)
    sell_qty = round_down(exec_qty, ROUND_QUANTITY)

    # --- Calculate Sell Price ---
    sell_price = round(market_price * (1 + profit_percent / 100), 6)

    # --- Place Limit Sell ---
    sell_order_id = place_limit_sell(pair, sell_qty, sell_price)
    if sell_order_id:
        print(f"[SUCCESS] Sell order placed. ID: {sell_order_id}")
        # --- Print balances ---
        try:
            balance = client.get_wallet_balance(accountType="spot")
            coins = balance["result"]["list"][0]["coin"]

            coin_bal = next((c for c in coins if c["coin"] == pair.replace("USDT", "")), {"walletBalance": "0"})
            usdt_bal = next((c for c in coins if c["coin"] == "USDT"), {"walletBalance": "0"})

            print(f"\nAfter trade balances:")
            print(f"→ {coin_bal['coin']}: {coin_bal['walletBalance']}")
            print(f"→ USDT: {usdt_bal['walletBalance']}\n")

        except Exception as e:
            print(f"[WARN] Failed to fetch balances: {e}")
    else:
        print("[FAIL] Failed to place sell order.")

if __name__ == "__main__":
    main()
