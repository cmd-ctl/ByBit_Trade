import datetime
import os
import time
import json
import math
from dotenv import load_dotenv
from past.builtins import raw_input
from pybit.unified_trading import HTTP
import logging
import balance

logging.basicConfig(filename="snipe_system.log", level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s %(message)s")

def connect():
    load_dotenv()

    BYBIT_API_KEY = os.environ.get("API_KEY")
    BYBIT_API_SECRET = os.environ.get("SECRET")
    TESTNET = False  # True means your API keys were generated on testnet.bybit.com

    session = HTTP(
        api_key=BYBIT_API_KEY,
        api_secret=BYBIT_API_SECRET,
        testnet=TESTNET,
    )
    return session

def main():

    load_dotenv()
    print("Starting program...\nNotice: only for SPOT trading\n")

    # Set ticker
    sym = os.environ.get("TICKER")

    def chk_price():
        data = session.get_tickers(
            category="spot",
            symbol=sym,
        )
        tkr = json.dumps(data)
        b = json.loads(tkr)
        ti = b['result']
        tik = ti['list']
        tick = tik[0]
        tickerB = tick['bid1Price']
        tickerA = tick['ask1Price']
        print("--- " + sym + " ---\nCurrent prices:\nBidPrice: " + tickerB + "\nAskPrice: " + tickerA + "\n---")
        return tickerB

    # check current price
    session = connect()
    try:
        chk_price()
    except Exception as e:
        print("Ticker data not found in listing! Trade pair may not exist.\n[ERR]: " + str(e) + "\n")

# -----------  USER SETTINGS  -----------
    # Set sell limit price
    print("Set sell limit-order price:")
    tpp = input()
    # Set amount in USDT & sell amount count
    print("Set the Amount (in basic token):")
    qty = input()
    # Stop price
    print("Set Stop-buy price:")
    abt = float(input())
    # Set time
    print("\nEnter the time to start:\n(YYYY, MM, DD, HH, MM)")
    t2 = datetime.datetime.strptime(raw_input(""), '%Y, %m, %d, %H, %M')
# -----------  END USER SETTINGS ZONE  -----------

    global k
    k = True
    global tickerC

    while k == True:
        # Timer count
        t_now = datetime.datetime.now()
        if t2 < t_now:

            # Start trade action
            session = connect()
            try:
                tB = chk_price()
                tickerC = float(tB)
            except Exception as e:
                print(" >> Check prices failed:\n" + str(e))

            # Check if Current price under the Stop-buy price
            if tickerC >= abt:
                print("Buy order won't be complete:")
                print("Current price: " + str(tickerC) + "\nStop price: " + str(abt))

            else:
                # Place Buy Market-order
                try:
                    response = session.place_order(
                        category="spot",
                        symbol=sym,
                        side="Buy",
                        orderType="Market",
                        qty=qty,
                        timeInForce="GTC",
                    )
                    print(" >> Buy order successful ")
                except Exception as e:
                    print(" >> Buy order failed:\n" + str(e))

                # Updating prices & count sell amount
                tB = chk_price()
                sqt = math.floor(float(qty) / float(tB) / float(os.environ.get("ROUND_QUANTITY"))) * float(os.environ.get("ROUND_QUANTITY"))

                # Account Balance check
                balance.chk_balance()
                print( " " + sym + " amount for sell: " + str(sqt))

                # Placing Sell Limit-order
                try:
                    response = session.place_order(
                        category="spot",
                        symbol=sym,
                        side="Sell",
                        orderType="Limit",
                        price=tpp,
                        qty=str(sqt),
                        timeInForce="GTC",
                    )
                    print(" >> Sell Limit-order placed ")
                except Exception as e:
                    print(" >> Sell order placing failed:\n" + str(e))

            # Close program
            k = False
            print("<Press -Enter- for exit>")
            input()

        else:
            # Count the time before action
            delta = t2 - t_now
            print('Time remaining: ' + str(delta))
            time.sleep(5)

if __name__ == "__main__":
    main()
