__all__=['initialize']
import pandas as pd
from constants import *
from BinanceKeys import *
from binance.client import Client
import data_grab as dg
import numpy as np
def initialize():
    """
    Initializes the dataframe with the 500 last intervals.
    Takes intervals from the constants functions.

    Args:
        none.
        
    Returns
        dataframe: 500 last prices and the SMA20 and EMA15.
    """
    client = Client(key(), secretKey())
    df_init = dg.xgrab_rate(symbol(), interval())
    df = pd.DataFrame(np.nan, index=range(0, 500), columns=["price"])
    df_init["c"] = df_init["c"].astype(float)
    for i in range(0, 500):
        df.iloc[i, 0] = df_init.iloc[i, 4]
    df = df.sort_index(axis=0, ascending=True)
    balanceBUSD = client.get_asset_balance(asset="BUSD")
    balanceBNB = client.get_asset_balance(asset="BNB")
    balanceBUSD = float(balanceBUSD["free"])
    balanceBNB = float(balanceBNB["free"])
    df["amt_BUSD"] = np.nan
    df["amt_BNB"] = np.nan
    SMA_hist = df["price"].ewm(span=short_span(), adjust=False).mean()
    df["EMA15"] = SMA_hist
    SMA_hist = df.iloc[:, 0].rolling(20).mean()
    df["SMA20"] = SMA_hist
    return df

if __name__=="__main__":
    print(initialize())