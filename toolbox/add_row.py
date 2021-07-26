from initialize import initialize
import pandas as pd
import numpy as np
from constants import *
import data_grab as dg
def add_row(df):
    '''
    Adds a row to the dataframe in the last position (n-th position, n=len(df)).
    Returns the dataframe with added row
    '''
    n=len(df)
    top_row = pd.DataFrame(
        {
            "price": [np.nan],
            "amt_BUSD": [np.nan],
            "amt_BNB": [np.nan],
            "EMA15": [np.nan],
            "SMA20": [np.nan],
        }
    )
    df = pd.concat([df, top_row]).reset_index(drop=True)
    df["price"][n] = dg.xgrab_live(symbol())  # adding a row
    # SMA
    SMA_hist = df["price"].ewm(span=shortSpan(), adjust=False).mean()
    df["EMA15"] = SMA_hist
    SMA_hist = df["price"].rolling(20).mean()
    df["SMA20"] = SMA_hist
    return df

if __name__ == "__main__":
    df=initialize()
    print(add_row(df))