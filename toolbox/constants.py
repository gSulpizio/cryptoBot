def symbol():
    '''returns the traded symbol (ex: BNBUSDT)'''
    return "BNBBUSD"
def interval():
    '''returns the time interval'''
    return "1h"
def rounding():
    '''returns the minimum rounding that has to be done, is specific for traded symbol pair'''
    return 4
def shortSpan():
    '''returns the span of the short average'''
    return 15

if __name__ == "__main__":
    print(symbol())
    print(interval())
    print(rounding())
    print(shortSpan())