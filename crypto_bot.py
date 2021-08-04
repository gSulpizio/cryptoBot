from parameters import *
from initialize import initialize
from Push_notification import push
from add_row import add_row
from balances import balances
from sell_condition import sell_condition
from buy_condition import buy_condition
from binance_order import binance_order
from database import create, add_row_to_db

from datetime import datetime
import time
"""
Runs the whole algorithm, to make the documentation comment the sleep functions and uncomment the break
"""
if database():
    create()
df=initialize()
MSG = f"Initiating trading {symbol()} 1h using EMA"
push(MSG)
amt1, amt2=balances(df)
total_initial=amt1+amt2
bought_price=0


while True:
    #break #uncomment for doc building
    if datetime.now().minute!=0:
        time.sleep(60)
        continue
    action='-'
    df=add_row(df)
    amt1, amt2=balances(df)
    if amt2>amt1 and buy_condition(df):
        binance_order(symbol(), amt2, "BUY")
        push(f"BUY, price: {df['price'][len(df)-1]}, @: {datetime.now()}")
        action='BUY'
        bought_price=df['price'][len(df)-1]
    if amt1>amt2 and sell_condition(df):
        binance_order(symbol(), amt2, "BUY")
        rtrn=round(df['price'][len(df)-1]/bought_price, 2)
        push(f"SELL, price: {df['price'][len(df)-1]}, return: {rtrn}% @:',{datetime.now()}")
        action='SELL'
    df["amt_BUSD"][len(df)-1] = amt2
    df["amt_BNB"][len(df)-1] = amt1
    if(database()):
        price=df['price'][len(df)-1]
        money=(amt2+amt1)*price
        add_row_to_db(price, df['long_avg'][len(df)-1], df['short_avg'][len(df)-1], money, action)
    time.sleep(round(interval_seconds()*0.5,0))
 