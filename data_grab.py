import datetime as dt
from binance.client import Client
import BinanceKeys as BKeys
import pandas as pd
import json  # for parsing what binance sends back to us
import numpy as np  # numerical python, i usually need this somewhere
import requests
import CustomFunctions
import time as tm
import matplotlib.pyplot as plt  # for charts and such

client = Client(BKeys.key(), BKeys.SecretKey())


def xgrab_rate(symbol, interval):

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
    prices_prov = client.get_all_tickers()
    prices = pd.DataFrame(prices_prov)
    lin = prices.index[prices["symbol"].str.contains(symbol)]
    lin = lin[0]
    prices["price"] = prices["price"].astype(float)
    p = prices.iloc[lin, 1]
    return p


def xgrab_live_v2(symbol):
    try:
        root_url = "https://api.binance.com/api/v1/ticker/price"
        url_1 = root_url + "?symbol=" + symbol
        url = requests.get(url_1)
        price = url.json()
        p = float(price["price"])
        return p
    except:
        tm.sleep(10 * 60)
        xgrab_live_v2(symbol)
