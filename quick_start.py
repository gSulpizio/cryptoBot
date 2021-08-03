import json
from binance.client import Client
from binance.helpers import interval_to_milliseconds

from math import log10

from BinanceKeys import *
client = Client(key(), secretKey())


"""Sets up the script: writes txt file with public and secret binance keys as well as a settings txt file with user input into the settings folder"""
def start_keys():
    """Writes the public and private API keys into ./settings/keys.json"""
    #if not os.path.exists('./settings/keys.txt'):
    print('API keys not set up,')
    print('Please enter public Binance api key:')
    public=input()
    print('Please enter secret Binance api key:')
    secret=input()
    with open('settings/keys.json', 'w+') as f:
        json.dump({'public':public, 'secret':secret},f)
    print("Done!")


def start_parameters():
    """Writes the parameters into ./settings/parameters.json"""
    print('Creating Settings:')
    symbol1=input('Please enter the first symbol of the traded pair (in BTCUSDT, this would be BTC):\n').upper()
    symbol2=input('Please enter the second symbol of the traded pair (in BTCUSDT, this would be USDT):\n').upper()
    interval=input('Please type in a custom interval, chosen from:  1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d\n')    
    rounding=int((-log10(float(client.get_symbol_info(symbol1+symbol2)['filters'][2]['stepSize']))))
    short_span=input('Please enter (in interval units) the short exponential moving average window:\n')
    long_span=input('Please enter (in interval units) the long simple moving average window\n')
    parameters={'asset1':symbol1, 'asset2':symbol2,'interval':interval, 'short_span':short_span,'long_span':long_span, 'rounding':rounding}
    with open('settings/parameters.json', 'w+') as f:
        json.dump(parameters,f)
    print("Done!")

if __name__=="__main__":
    start_keys()
    start_parameters()