__all__=['key', 'SecretKey']
def key():
    '''
    Returns public api key for binance
    '''
    a='JzrKFJZZeg274N9uTMTRdfqtruipvIE2M6rR1ohYBcVcw2lYVA6d5Q0jVg8asTSC'
    return a

def SecretKey():
    '''
    Returns private api key for binance
    '''
    b='5tHCL85UtoGwLeX13tyICx6lj2C4dBO2Klw1JkISzgHn1k3LQCi55IPcmHKF9ZiA'
    return b

if __name__ == "__main__":
    print(key())
    print(SecretKey())
