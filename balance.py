import json
import snipe

def chk_balance():
    session = snipe.connect()

    data = session.get_wallet_balance(accountType="spot")
    wbal = json.dumps(data)
    b = json.loads(wbal)
    balance = b['result']
    wb = balance['list']
    wwb = wb[0]
    wwbb = wwb['coin']

    print("\nCurrent wallet balance:\n---")
    for i in wwbb:
        print("Coin: " + i['coin'] + " -> " + i['walletBalance'])
    print("---")

