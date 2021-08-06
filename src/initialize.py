__all__=['initialize']
import pandas as pd
from parameters import *
from BinanceKeys import *
from binance.client import Client
import data_grab as dg
import numpy as np
def initialize():
    """
    Initializes the dataframe with the 500 last intervals.
    Takes intervals from the parameters functions.

    Args:
        none.
        
    Returns
        dataframe: 500 last prices and the long_avg and short_avg.
    """
    client = Client(key(), secretKey())
    df_init = dg.xgrab_rate(symbol(), interval())
    df = pd.DataFrame(np.nan, index=range(0, 500), columns=["price"])
    df_init["c"] = df_init["c"].astype(float)
    for i in range(0, 500):
        df.iloc[i, 0] = df_init.iloc[i, 4]
    df = df.sort_index(axis=0, ascending=True)
    balance2 = client.get_asset_balance(asset=asset2())
    balance1 = client.get_asset_balance(asset=asset1())
    balance2 = float(balance2["free"])
    balance1 = float(balance1["free"])
    df["amt_2"] = np.nan
    df["amt_1"] = np.nan
    SMA_hist = df["price"].ewm(span=short_span(), adjust=False).mean()
    df["short_avg"] = SMA_hist
    SMA_hist = df.iloc[:, 0].rolling(20).mean()
    df["long_avg"] = SMA_hist
    return df

if __name__=="__main__":
    print(initialize())