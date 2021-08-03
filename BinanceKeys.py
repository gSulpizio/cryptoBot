"""Reads from keys.txt that can be generated with quick_start.py"""
keys=open("settings/keys.txt").read().splitlines()
def key():
    """Returns public api key for binance
    
    Returns:
        string

    """
    return keys[0]

def secretKey():
    """Returns private api key for binance
    
    Returns:
        string

"""
    return keys[1]

if __name__ == "__main__":
    print(key())
    print(secretKey())
