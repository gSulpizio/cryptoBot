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
import ccxt
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
w = 60*60*24  # change back to 1 H, 3s is for testing
x = 0.001
bprice = 0

# print('enter amount of days')
# n_prov=float(input())*24

symbol = 'BTCUSDT'

# initialisation:

df = pd.DataFrame()
df_init = dg.xgrab_rate(symbol)

df = pd.DataFrame(np.nan, index=range(0, 500), columns=['price'])
df_init['c'] = df_init['c'].astype(float)

for i in range(0, 500):
    df.iloc[i, 0] = df_init.iloc[i, 4]

df = df.sort_index(axis=0, ascending=True)

balanceUSDT = client.get_asset_balance(asset='USDT')
balanceBTC = client.get_asset_balance(asset='BTC')
balanceUSDT = float(balanceUSDT['free'])
balanceBTC = float(balanceBTC['free'])
money_fix = balanceBTC + balanceUSDT / df.iloc[0, 0]

df['amt_USDT'] = np.nan
df['amt_BTC'] = np.nan


# EMA:

EMA_hist = df.iloc[:, 0].ewm(span=8, adjust=False).mean()
df['EMA8'] = EMA_hist
EMA_hist = df.iloc[:, 0].ewm(span=13, adjust=False).mean()
df['EMA13'] = EMA_hist
EMA_hist = df.iloc[:, 0].ewm(span=21, adjust=False).mean()
df['EMA21'] = EMA_hist
EMA_hist = df.iloc[:, 0].ewm(span=55, adjust=False).mean()
df['EMA55'] = EMA_hist


n = len(df)

MSG = (f"Initiating trading {symbol} 24h using EMA")
psh.push(MSG)

tm.sleep(w)


# loop:
while True == True:
    top_row = pd.DataFrame(
        {'price': [np.nan], 'RSI': [np.nan], 'amt_USDT': [np.nan],
         'amt_BTC': [np.nan], 'EMA8': [np.nan], 'EMA13': [np.nan], 'EMA21': [np.nan], 'EMA55': [np.nan]})
    df = pd.concat([df, top_row]).reset_index(drop=True)
    df.iloc[n, 0] = dg.xgrab_live_v2(symbol)  # adding a row
# EMA
    EMA_hist = df.iloc[:, 0].ewm(span=8, adjust=False).mean()
    df['EMA8'] = EMA_hist
    EMA_hist = df.iloc[:, 0].ewm(span=13, adjust=False).mean()
    df['EMA13'] = EMA_hist
    EMA_hist = df.iloc[:, 0].ewm(span=21, adjust=False).mean()
    df['EMA21'] = EMA_hist
    EMA_hist = df.iloc[:, 0].ewm(span=55, adjust=False).mean()
    df['EMA55'] = EMA_hist

    balanceUSDT = client.get_asset_balance(asset='USDT')
    balanceBTC = client.get_asset_balance(asset='BTC')
    balanceUSDT = float(balanceUSDT['free'])
    balanceBTC = float(balanceBTC['free'])

    balanceUSDT = balanceUSDT / df.iloc[n, 0]  # converting to BTC

    amt_BTC = balanceBTC * 0.99
    amt_USDT = balanceUSDT * 0.99  # it's in BTC

    if not (act == 0):
        act = act - 1
    if amt_USDT >= amt_BTC:
        if CustomFunctions.buy_conditions_EMA_f(df, n) == True:  # buy BTC
            client.order_market_buy(symbol=symbol, quantity=round(amt_USDT, 6))
            rt = (balanceUSDT + balanceBTC) / money_fix * 100
            MSG = (
                f"BUY, price: {df.iloc[n, 0]},return: {rt} '% @:',{dt.datetime.now()}")
            psh.push(MSG)
            act = 2
            bprice = df.iloc[n, 0]

    if amt_BTC >= amt_USDT:  # if we activate the if above, transform if to elif
        # Did SMA get smaller than closing price?
        if CustomFunctions.sell_conditions_EMA_f(df, n) == True:  # sell BTC
            client.order_market(symbol=symbol, side='SELL',
                                quantity=round(amt_BTC, 6))
            rt = (balanceUSDT + balanceBTC) / money_fix * 100
            MSG = (
                f"SELL, price: {df.iloc[n, 0]},return: {rt} '% @:',{dt.datetime.now()}")
            psh.push(MSG)
            if df.iloc[n, 0] < 0.99 * bprice:
                act = 10
            else:
                act = 2

    df.iloc[n, 2] = amt_USDT
    df.iloc[n, 3] = amt_BTC

    n += 1
    tm.sleep(w)
