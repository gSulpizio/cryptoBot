import datetime as dt
from binance.client import Client
import pandas as pd
import json  # for parsing what binance sends back to us
import numpy as np  # numerical python, i usually need this somewhere
import requests
import CustomFunctions
import matplotlib.pyplot as plt  # for charts and such
import time as tm
import data_grab as dg
import BinanceKeys as BKeys
#import ccxt
import Push_notification as psh
#import pickle
import os.path


# orders

client = Client(BKeys.key(), BKeys.SecretKey())

# testing settings                                                                                                                #testing settings

rad_avgday = 14
rad_2nd_avg = 2
trade_margin = 0.01
fee = 0.001
act = 1
w = 60*60  # change back to 1 H, 3s is for testing
x = 0.001
bprice = 0

# print('enter amount of days')
# n_prov=float(input())*24

symbol = 'BNBUSDT'

# initialisation:

df = pd.DataFrame()
df_init = dg.xgrab_rate(symbol)

df = pd.DataFrame(np.nan, index=range(0, 500), columns=['price'])
df_init['c'] = df_init['c'].astype(float)

for i in range(0, 500):
    df.iloc[i, 0] = df_init.iloc[i, 4]

df = df.sort_index(axis=0, ascending=True)

balanceUSDT = client.get_asset_balance(asset='USDT')
balanceBNB = client.get_asset_balance(asset='BNB')
balanceUSDT = float(balanceUSDT['free'])
balanceBNB = float(balanceBNB['free'])
money_fix = balanceBNB + balanceUSDT 

df['amt_USDT'] = np.nan
df['amt_BNB'] = np.nan


# SMA:

SMA_hist = df.iloc[:, 0].rolling(30).mean()
df['SMA30'] = SMA_hist
SMA_hist = df.iloc[:, 0].rolling(90).mean()
df['SMA90'] = SMA_hist

n = len(df)

MSG = (f"Initiating trading {symbol} 1h using EMA")
psh.push(MSG)
w=1
tm.sleep(w)


# loop:
while True == True:
    top_row = pd.DataFrame(
        {'price': [np.nan], 'amt_USDT': [np.nan],
         'amt_BNB': [np.nan], 'SMA30': [np.nan], 'SMA90': [np.nan]})
    df = pd.concat([df, top_row]).reset_index(drop=True)
    df['price'][n] = dg.xgrab_live_v2(symbol)  # adding a row
# SMA
    SMA_hist = df['price'].rolling(30).mean()
    df['SMA30'] = SMA_hist
    SMA_hist = df['price'].rolling(90).mean()
    df['SMA90'] = SMA_hist

    balanceUSDT = client.get_asset_balance(asset='USDT')
    balanceBNB = client.get_asset_balance(asset='BNB')
    balanceUSDT = float(balanceUSDT['free'])
    balanceBNB = float(balanceBNB['free'])

    balanceUSDT = balanceUSDT / df['price'][n]  # converting to BNB

    amt_BNB = balanceBNB * 0.99
    amt_USDT = balanceUSDT * 0.99  # it's in BNB
    MSG = (f"short moving average: {df['SMA30'][n]}, long moving average: {df['SMA90'][n]}")
    psh.push(MSG)
    if not (act == 0):
        act = act - 1
    if amt_USDT >= amt_BNB:
        if CustomFunctions.buy_conditions_SMA(df, n) == True:  # buy BNB
            client.order_market_buy(symbol=symbol, quantity=round(amt_USDT, 6))
            rt = (balanceUSDT + balanceBNB) / money_fix * 100
            MSG = (
                f"BUY, price: {df['price'][n]},return: {rt} '% @:',{dt.datetime.now()}")
            psh.push(MSG)
            act = 2
            bprice = df['price'][n]

    if amt_BNB >= amt_USDT:  # if we activate the if above, transform if to elif
        # Did SMA get smaller than closing price?
        if CustomFunctions.sell_conditions_SMA(df, n) == True:  # sell BNB
            client.order_market(symbol=symbol, side='SELL',
                                quantity=round(amt_BNB, 6))
            rt = (balanceUSDT + balanceBNB) / money_fix * 100
            MSG = (
                f"SELL, price: {df['price'][n]},return: {rt} '% @:',{dt.datetime.now()}")
            psh.push(MSG)
            if df['price'][n] < 0.99 * bprice:
                act = 10
            else:
                act = 2

    df['amt_USDT'][n] = amt_USDT
    df['amt_BNB'][n] = amt_BNB

    n += 1
    tm.sleep(w)
