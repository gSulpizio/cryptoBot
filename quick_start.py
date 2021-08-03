import os
from binance.client import Client
from binance.helpers import interval_to_milliseconds

from math import log10

from BinanceKeys import *
client = Client(key(), secretKey())


"""Sets up the script: writes txt file with public and secret binance keys as well as a settings txt file with user input into the settings folder"""
def start_keys():
    """Writes the public and private API keys into ./settings/keys.txt"""
    #if not os.path.exists('./settings/keys.txt'):
    print('API keys not set up,')
    print('Please enter public Binance api key:')
    public=input()
    print('Please enter secret Binance api key:')
    private=input()
    with open('settings/keys.txt', 'w+') as f:
        f.write(public+'\n'+private)
    print('Creating Settings:')
    symbol1=input('Please enter the first symbol of the traded pair (in BTCUSDT, this would be BTC):\n').upper()
    symbol2=input('Please enter the second symbol of the traded pair (in BTCUSDT, this would be USDT):\n').upper()
    interval=input('Please type in a custom interval, chosen from:  1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d\n')    rounding=int((-log10(float(client.get_symbol_info(symbol1+symbol2)['filters'][2]['stepSize']))))
    short_span=input('Please enter (in interval units) the short exponential moving average window:\n')
    long_span=input('Please enter (in interval units) the long simple moving average window\n')
    with open('settings/constants.txt', 'w+') as f:
        f.write(symbol1+'\n'+symbol2+'\n'+interval+'\n'+str(rounding)+'\n'+str(short_span)+'\n'+str(long_span))
    print("Done!")
'''
from BinanceKeys import *
def other_fn():
    client = Client(key(), secretKey())
    if not os.path.exists('./settings/constants.txt'):
        """Writes the constants (symbol,) into ./settings/constants.txt"""
        print('No settings found, will be set up now:')
        symbol1=input('please enter the first symbol of the traded pair (in BTCUSDT, this would be BTC):\n').upper()
        symbol2=input('please enter the second symbol of the traded pair (in BTCUSDT, this would be USDT):\n').upper()
        rounding2=int((-log10(float(client.get_symbol_info(symbol1+symbol2)['filters'][2]['stepSize']))))
        print(rounding2)
'''
start_keys()