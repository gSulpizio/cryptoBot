"""Reads from keys.json that can be generated with quick_start.py"""
import json
try:
    f=open('settings/keys.json')
    keys=json.load(f)
    f.close()
except: 
    keys={'public':'', 'secret':''}

def key():
    """Returns public api key for binance
    
    Returns:
        string

    """
    return keys['public']

def secretKey():
    """Returns private api key for binance
    
    Returns:
        string

"""
    return keys['secret']

if __name__ == "__main__":
    print(key())
    print(secretKey())
