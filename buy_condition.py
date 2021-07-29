def buy_condition(df):
    '''
    Checks if buying conditions are met for the SMA
    - df: dataframe containing SMA20 and EMA15
    Returns boolean
    '''
    n=len(df)-1
    EMA15 = df["EMA15"][n]
    SMA20 = df["SMA20"][n]
    pEMA15 = df["EMA15"][n - 1]
    pSMA20 = df["SMA20"][n - 1]
    if EMA15 > SMA20 and pEMA15 < pSMA20:
        return True
    else:
        return False


if __name__ == "__main__":
    from initialize import initialize
    df=initialize()
    print(buy_condition(df))
