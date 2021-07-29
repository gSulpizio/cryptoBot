from binance.client import Client
import BinanceKeys as BKeys
from constants import *
def balances(df):
    '''
    Gets balances of both assets
    '''
    n=len(df)-1
    client = Client(BKeys.key(), BKeys.SecretKey())
    balance2 = client.get_asset_balance(asset=asset2())
    balance1 = client.get_asset_balance(asset=asset1())
    balance2 = float(balance2["free"])
    balance1 = float(balance1["free"])

    balance2 = balance2 / df["price"][n]  # converting to BNB

    amt1 = balance1 * 0.99
    amt2 = balance2 * 0.99  # it's in amt2
    return amt1,amt2