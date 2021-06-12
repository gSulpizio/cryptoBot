from binance.client import Client
import datetime as dt
import time as tm
import BinanceKeys as BKeys
import Push_notification as psh

client = Client(BKeys.key(), BKeys.SecretKey())


def sell_order(pair, quantity):
    counter = 0
    order = client.order_market(symbol=pair, quantity=quantity, side="SELL")
    status = order["status"]
    while True:
        if status != "FILLED" and counter < 10:
            tm.sleep(15)
            order = client.order_market(symbol=pair, quantity=quantity, side="SELL")
            status = order["status"]
        elif counter == 10:
            psh.push("SELL ORDER COULD NOT BE PLACED")
        else:
            break


def buy_order(pair, quantity):
    counter = 0
    order = client.order_market(symbol=pair, quantity=quantity, side="BUY")
    status = order["status"]
    while True:
        if status != "FILLED" and counter < 10:
            tm.sleep(15)
            order = client.order_market(symbol=pair, quantity=quantity, side="BUY")
            status = order["status"]
        elif counter == 10:
            psh.push("BUY ORDER COULD NOT BE PLACED")
        else:
            return
