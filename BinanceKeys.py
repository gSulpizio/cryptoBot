"""Reads from keys.txt that can be generated with quick_start.py"""
keys=open("keys.txt").read().splitlines()
def key():
    """Returns public api key for binance
    
    Returns:
        string

    """
    return keys[0]

def SecretKey():
    """Returns private api key for binance
    
    Returns:
        string

"""
    return keys[1]

if __name__ == "__main__":
    print(key())
    print(SecretKey())
