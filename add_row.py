from initialize import initialize
import pandas as pd
import numpy as np
from parameters import *
import data_grab as dg


def add_row(df):
    """
    Adds a row to the dataframe in the last position (n-th position, n=len(df)).

    Args:
        df (dataframe): dataframe of prices until now.

    Returns: 
        df (dataframe): dataframe of prices until now plus live price in last position.
    """
    n = len(df)
    top_row = pd.DataFrame(
        {
            "price": [np.nan],
            "amt_BUSD": [np.nan],
            "amt_BNB": [np.nan],
            "short_avg": [np.nan],
            "long_avg": [np.nan],
        }
    )
    df = pd.concat([df, top_row]).reset_index(drop=True)
    df["price"][n] = dg.xgrab_live(symbol())  # adding a row
    # SMA
    df["short_avg"] = df["price"].ewm(span=short_span(), adjust=False).mean()
    df["long_avg"] = df["price"].rolling(long_span()).mean()
    return df


if __name__ == "__main__":
    df = initialize()
    print(add_row(df))
