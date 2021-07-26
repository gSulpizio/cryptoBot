import datetime as dt
from constants import interval, symbol
from binance.client import Client
import BinanceKeys as BKeys
import pandas as pd
import json  # for parsing what binance sends back to us
import numpy as np  # numerical python, i usually need this somewhere
import requests
import CustomFunctions
import time as tm

client = Client(BKeys.key(), BKeys.SecretKey())


def xgrab_rate(symbol, interval):
    '''
    Returns 500 last rates in a dataframe
    param: {string} symbol - symbol of the coins (ex: BNBBUSD)
    param: {string} interval - time interval (ex: 1h)
    '''

    root_url = "https://api.binance.com/api/v1/klines"

    # interval = '1h'

    url = root_url + "?symbol=" + symbol + "&interval=" + interval

    data = json.loads(requests.get(url).text)

    df = pd.DataFrame(data)
    df.columns = [
        "open_time",
        "o",
        "h",
        "l",
        "c",
        "v",
        "close_time",
        "qav",
        "num_trades",
        "taker_base_vol",
        "taker_quote_vol",
        "ignore",
    ]

    df.index = [dt.datetime.fromtimestamp(x / 1000.0) for x in df.close_time]

    def get_bars(symbol, interval=interval):
        url = root_url + "?symbol=" + symbol + "&interval=" + interval
        data = json.loads(requests.get(url).text)
        df = pd.DataFrame(data)
        df.columns = [
            "open_time",
            "o",
            "h",
            "l",
            "c",
            "v",
            "close_time",
            "qav",
            "num_trades",
            "taker_base_vol",
            "taker_quote_vol",
            "ignore",
        ]
        df.index = [dt.datetime.fromtimestamp(x / 1000.0) for x in df.close_time]
        return df

    steemeth = get_bars("STEEMETH")
    ethusdt = get_bars("ETHUSDT")

    steemusdt = steemeth["c"].astype("float") * ethusdt["c"].astype("float")

    return df

def xgrab_live(symbol):
    '''
    Returns the rate of the symbol
    '''
    try:
        root_url = "https://api.binance.com/api/v1/ticker/price"
        url_1 = root_url + "?symbol=" + symbol
        url = requests.get(url_1)
        price = url.json()
        p = float(price["price"])
        return p
    except:
        tm.sleep(10 * 60)
        xgrab_live(symbol)

if __name__=="__main__":
    symbol='BNBBUSD'
    interval='1h'
    print(xgrab_rate(symbol, interval))
    print(xgrab_live(symbol))