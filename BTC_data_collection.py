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
import pickle
import os.path
import tulipy as ti

w=60

client = Client(BKeys.key(), BKeys.SecretKey())

symbol = 'BTCBUSD'


n=0
df=pd.DataFrame({'price': [np.nan]})

if not (os.path.exists('datacollection.pckl')):
    # f = open('store.pckl', 'wb', encoding="utf8")
    # pickle.dump(df, f)
    # f.close()
    df.to_pickle('datacollection.pckl')

while True==True:
    top_row = pd.DataFrame({'price': [np.nan]})
    df = pd.concat([df, top_row]).reset_index(drop=True)
    df.iloc[n, 0] = dg.xgrab_live_v2(symbol)  # adding a row

    data_dump = pd.read_pickle('datacollection.pckl')
    top_row = pd.DataFrame(
        {'price': [np.nan]})
    data_dump = pd.concat([top_row, data_dump]).reset_index(drop=True)

    data_dump.iloc[n, 0] = df.iloc[n, 0]  # adding a row

    df.to_pickle('datacollection.pckl')
    n += 1
    tm.sleep(w)
