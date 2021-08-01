from binance.client import Client
from constants import rounding
import datetime as dt
import time as tm
import BinanceKeys as BKeys
import Push_notification as psh
def binance_order(pair, quantity,side, timeout=10):
    """
    Sends a buy or sell request to Binance.

    Args:
        pair (string): string of trading pair (ex: 'BNBUSDT').
        quantity (float): amount of the first member of the pair to trade.
        side (string): "BUY" to buy BNB and "SELL" to sell BNB for the example.
        timeout (int): if the request fails, the amount of time (in minutes) to wait before retrying.
    
    Returns: void
    """
    client = Client(BKeys.key(), BKeys.SecretKey())
    order_quantity=round(quantity, rounding())
    try:
        order = client.order_market(symbol=pair, quantity=order_quantity, side=side)
        status = order["status"]
        if status == "FILLED":
            return
    except: 
        tm.sleep(timeout*60)
        order = client.order_market(symbol=pair, quantity=order_quantity, side=side)
        status = order["status"]
        if status == "FILLED":
            return
        else: 
            psh.push("CAN'T FILL "+side+" ORDER")
            raise("CAN'T FILL "+side+" ORDER")

if __name__ == "__main__":
    print("protected, can't launch orders on its own")
