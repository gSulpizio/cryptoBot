from binance.helpers import interval_to_milliseconds
import json

f=open('settings/parameters.json')
parameters=json.load(f)
f.close()

def asset1():
    """returns the first traded asset (ex: BNB in BNBUSDT)
    
    Returns:
        string
"""
    return parameters['asset1']
def asset2():
    """returns the second traded asset (ex: USDT in BNBUSDT)
    
    Returns:
        string
"""
    return parameters['asset2']
def symbol():
    """returns the traded symbol (ex: BNBUSDT)
    
    Returns:
        string
"""
    return asset1()+asset2()
def interval():
    """returns the time interval as a string:
    1m, 3m, 5m, 15m, 30m, 1h, 2h, 4h, 6h, 8h, 12h, 1d, 3d
    
    Returns:
        string
"""
    return parameters['interval']
def interval_seconds():
    """returns the time interval in seconds
    
    Returns:
        int
"""
    return int(interval_to_milliseconds(interval())/1000)

def rounding():
    """returns the minimum rounding that has to be done, is specific for traded symbol pair
    
    Returns:
        string
"""
    return int(parameters['rounding'])
def short_span():
    """returns the span of the short average
    
    Returns:
        string
"""
    return int(parameters['short_span'])
def long_span():
    """returns the span of the long average
    
    Returns:
        string
"""
    return int(parameters['long_span'])

if __name__ == "__main__":
    print(symbol())
    print(interval())
    print(rounding())
    print(interval())
    print(interval_seconds())
    print(short_span())
    print(long_span())

