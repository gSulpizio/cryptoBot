constants=open("settings/constants.txt").read().splitlines()
from binance.helpers import interval_to_milliseconds


def asset1():
    """returns the first traded asset (ex: BNB in BNBUSDT)
    
    Returns:
        string
"""
    return constants[0]
def asset2():
    """returns the second traded asset (ex: USDT in BNBUSDT)
    
    Returns:
        string
"""
    return constants[1]
def symbol():
    """returns the traded symbol (ex: BNBUSDT)
    
    Returns:
        string
"""
    return asset1()+asset2()
def interval():
    """returns the time interval
    
    Returns:
        string
"""
    return constants[2]
def interval_seconds():
    """returns the time interval
    
    Returns:
        string
"""
    return int(interval_to_milliseconds(constants[2])/1000)

def rounding():
    """returns the minimum rounding that has to be done, is specific for traded symbol pair
    
    Returns:
        string
"""
    return int(constants[3])
def short_span():
    """returns the span of the short average
    
    Returns:
        string
"""
    return int(constants[4])
def long_span():
    """returns the span of the long average
    
    Returns:
        string
"""
    return int(constants[5])

if __name__ == "__main__":
    print(symbol())
    print(interval())
    print(rounding())
    print(short_span())