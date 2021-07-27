#__all__=['symbol', 'interval', 'rounding','shortSpan']
def symbol():
    '''returns the traded symbol (ex: BNBUSDT)'''
    return "BNBBUSD"
def interval():
    '''returns the time interval'''
    return "1h"
def rounding():
    '''returns the minimum rounding that has to be done, is specific for traded symbol pair'''
    return 4
def short_span():
    '''returns the span of the short average'''
    return 15
def long_span():
    '''returns the span of the long average'''
    return 20

if __name__ == "__main__":
    print(symbol())
    print(interval())
    print(rounding())
    print(short_span())