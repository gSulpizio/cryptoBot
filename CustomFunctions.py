def SMAcalc_binance(begin,days, data_for_SMA, target_column):
    SMA = 0
    start=begin+days-1
    stop=begin-1
    for i in range(start, stop, -1):
        SMA+=data_for_SMA.iloc[i,target_column]
    SMA=SMA/days
    return SMA


def EMAcalc_binance(n, days, data_for_EMA, target_column,prev_EMA):
    #start=begin+days-1
    #stop=begin-1
    fx=2/(1+days)
    EMA_p=prev_EMA
    EMA=fx*(data_for_EMA.iloc[n,target_column]-EMA_p)+EMA_p
#    EMA=EMA_p*(1-fx)+data_for_EMA.iloc[n, target_column]*fx
    return EMA


def rate_prompt(scale_input,rate_input,symb):
    import sys
    import time
    import pandas as pd
    import numpy as np
    from alpha_vantage.timeseries import TimeSeries
    import matplotlib.pyplot as plt
    ts = TimeSeries(key='U6HRHDW4N7XY52VM', output_format='pandas')
    if scale_input=='a':
        if rate_input=='a':
            data, meta_data = ts.get_intraday(symbol=symb,interval='1min', outputsize='full')
        elif rate_input=='b':
            data, meta_data = ts.get_intraday(symbol=symb,interval='5min', outputsize='full')
        elif rate_input=='c':
            data, meta_data = ts.get_intraday(symbol=symb,interval='15min', outputsize='full')
        elif rate_input=='d':
            data, meta_data = ts.get_intraday(symbol=symb,interval='30min', outputsize='full')
        else:
            sys.exit('rate input wrong')
    elif scale_input == 'b':
        data, meta_data = ts.get_daily(symbol=symb, outputsize='full')
    elif scale_input == 'c':
        data, meta_data = ts.get_weekly(symbol=symb, outputsize='full')
    else:
        sys.exit('scale input wrong')
    return data, meta_data

def momentum_calc(data):
    mom1=data.iloc[0, 3]/data.iloc[1, 3]*100
    mom2=data.iloc[1, 3]/data.iloc[2, 3]*100
    mom3 = data.iloc[2, 3] / data.iloc[3, 3] * 100
    mom4 = data.iloc[3, 3] / data.iloc[4, 3] * 100
    return mom1, mom2, mom3, mom4


def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.now().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else:  # crosses midnight
        return check_time >= begin_time or check_time <= end_time

def momentum_calc_test(day, data):
    day_a = day
    mom1 = data.iloc[day_a, 3] / data.iloc[day_a+1, 3] * 100
    mom2 = data.iloc[day_a+1, 3] / data.iloc[day_a+2, 3] * 100
    mom3 = data.iloc[day_a+2, 3] / data.iloc[day_a+3, 3] * 100
    mom4 = data.iloc[day_a+3, 3] / data.iloc[day_a+4, 3] * 100
    return mom1, mom2, mom3, mom4


def buy_conditions(df, n, trade_margin):
    upper_threshold = df.iloc[n, 17]
    lower_threshold = df.iloc[n, 16]
    upper_threshold_prev = df.iloc[n + 1, 17]
    lower_threshold_prev = df.iloc[n + 1, 16]
    df.iloc[n, 18] = upper_threshold * (1 + trade_margin)

    if (lower_threshold < df.iloc[n, 4] and lower_threshold_prev > df.iloc[n + 1, 4] and df.iloc[n + 1, 12] < df.iloc[n + 1, 4]):
        return True
    elif (upper_threshold * (1 + trade_margin) < df.iloc[n, 4] and upper_threshold_prev * (1 + trade_margin) > df.iloc[n + 1, 4]):  # and df.iloc[n+1,12]<df.iloc[n+1, 4]*(1-trade_margin):                                              #unused since we sell everything
        return True
    else:
        return False



def sell_conditions(df, n, trade_margin):
    upper_threshold = df.iloc[n, 17]
    lower_threshold = df.iloc[n, 16]
    upper_threshold_prev = df.iloc[n + 1, 17]
    lower_threshold_prev = df.iloc[n + 1, 16]
    df.iloc[n, 18] = upper_threshold * (1 + trade_margin)
    if upper_threshold > df.iloc[n, 4] and upper_threshold_prev < df.iloc[n + 1, 4]:
        return True
    else:
        return False



def buy_conditions_EMAmom(df, n, avg_EMA,pricecolumn):
    SMA=SMAcalc_binance(n,avg_EMA, df, pricecolumn)
    SMA_prev=SMAcalc_binance(n+1,avg_EMA, df, pricecolumn)
    SMA_prev2=SMAcalc_binance(n+2,avg_EMA, df, pricecolumn)
    SMA_prev3 = SMAcalc_binance(n + 3, avg_EMA, df, pricecolumn)
    if SMA>SMA_prev and SMA_prev<SMA_prev2 and SMA_prev2<SMA_prev3:
        return True
    else:
        return False



def sell_conditions_EMAmom(df, n, avg_EMA,pricecolumn):
    SMA=SMAcalc_binance(n,avg_EMA, df, pricecolumn)
    SMA_prev=SMAcalc_binance(n+1,avg_EMA, df, pricecolumn)
    SMA_prev2=SMAcalc_binance(n+2,avg_EMA, df, pricecolumn)
    SMA_prev3 = SMAcalc_binance(n + 3, avg_EMA, df, pricecolumn)
    if SMA<SMA_prev and SMA_prev>SMA_prev2: #and SMA_prev2>SMA_prev3:
        return True
    else:
        return False

def buy_conditions_4EMA(df, n, EMA8_col,EMA13_col,EMA21_col, EMA55_col):
    EMA8=df.iloc[n,EMA8_col]
    EMA13=df.iloc[n,EMA13_col]
    EMA21=df.iloc[n,EMA21_col]
    EMA55=df.iloc[n,EMA55_col]
    if EMA8>EMA13 and EMA13>EMA21 and EMA21>EMA55:
        return True
    else:
        return False

def sell_conditions_4EMA(df, n, EMA8_col,EMA13_col,EMA21_col, EMA55_col):
    EMA8=df.iloc[n,EMA8_col]
    EMA13=df.iloc[n,EMA13_col]
    EMA21=df.iloc[n,EMA21_col]
    EMA55=df.iloc[n,EMA55_col]
    if EMA8<EMA13 or EMA13<EMA21 or EMA21<EMA55:  # and SMA_prev2>SMA_prev3:
        return True
    else:
        return False

def sell_conditions_4EMA_1(df, n, EMA8_col,EMA13_col,EMA21_col, EMA55_col):
    EMA8=df.iloc[n,EMA8_col]
    EMA13=df.iloc[n,EMA13_col]
    EMA21=df.iloc[n,EMA21_col]
    EMA55=df.iloc[n,EMA55_col]
    if df.iloc[n+1,4]*1.02<df.iloc[n,4]:
       return True
    if EMA8<EMA13 or EMA13<EMA21 or EMA21<EMA55:  # and SMA_prev2>SMA_prev3:
        return True
    else:
        return False

def buy_conditions_MA(df,n, col_df):
    if df.iloc[n,4]<df.iloc[n,18]:# and df.iloc[n,4]>df.iloc[n,18]:# and df.iloc[n,12]>df.iloc[n+1,12]:# and df.iloc[n+1,col_df]<df.iloc[n+2,col_df] and df.iloc[n+2,col_df]<df.iloc[n+3,col_df]:
       return True
    else:
        return False

def sell_conditions_MA(df,n, bprice):
    if df.iloc[n,4] > df.iloc[n,17]:# and df.iloc[n+1,col_df]>df.iloc[n+2,col_df] and df.iloc[n+2,col_df]>df.iloc[n+3,col_df]:
       return True
    if df.iloc[n,4]<0.99*bprice:
        return True
    else:
        return False

def print_info(indicator):
    print("Type:", indicator.type)
    print("Full Name:", indicator.full_name)
    print("Inputs:", indicator.inputs)
    print("Options:", indicator.options)
    print("Outputs:", indicator.outputs)





def buy_conditions_RSI(df,n):
    RSI=df.iloc[n,12]
    if RSI<30:
        return True
    else:
        return False

def sell_conditions_RSI(df,n, bprice):
    RSI = df.iloc[n,12]
    if RSI>70:
       return True
    if df.iloc[n,4]<0.99*bprice:
        return True
    else:
        return False

def RSI_SMA(df,n,colprice, rad):#with simple moving avg. for EMA, change after the while
    upcounter=0
    downcounter=0
    upsum=0
    downsum=0
    n_count=n+rad-1
    while n_count>=0:
        if df.iloc[n_count, colprice]>df.iloc[n_count+1, colprice]:#up
            upcounter+=1
            upsum+=abs(df.iloc[n_count,colprice]-df.iloc[n_count+1,colprice])
        elif df.iloc[n_count, colprice]<df.iloc[n_count+1, colprice]:
            downcounter+=1
            downsum+=abs(df.iloc[n_count,colprice]-df.iloc[n_count+1,colprice])
        n_count=n_count-1

    avg_up=upsum/rad
    avg_down=downsum/rad

    RS=avg_up/avg_down
    RS_index=100-100/(1+RS)

    return RS_index



def EMAcalc_for_RSI(days, price,prev_EMA):
    fx=2/(1+days)
    EMA_p=prev_EMA
    EMA=fx*(price-EMA_p)+EMA_p
    return EMA


def RSI_EMA(df,n,colprice, rad):#with simple moving avg. for EMA, change after the while
    import numpy as np

    upcounter=0
    downcounter=0
    upsum=0
    downsum=0
    n_count=n+rad-1
    i=0
    j=0

    UPS=np.zeros(rad)
    DNS=np.zeros(rad)

    while n_count>=n:
        if df.iloc[n_count, colprice]>df.iloc[n_count+1, colprice]:#up
            UPS[i]=abs(df.iloc[n_count,colprice]-df.iloc[n_count+1,colprice])
            if upcounter==0:
                EMA_up=abs(df.iloc[n_count,colprice]-df.iloc[n_count+1,colprice])
            i+=1
            upcounter += 1

        elif df.iloc[n_count, colprice]<df.iloc[n_count-1, colprice]:
            DNS[j] = abs(df.iloc[n_count, colprice] - df.iloc[n_count + 1, colprice])
            if downcounter==0:
                EMA_down=abs(df.iloc[n_count,colprice]-df.iloc[n_count+1,colprice])
            downcounter += 1
            j+=1

        n_count=n_count-1

    #deleting 0 values:
    delete_counter = len(UPS) - 1
    while delete_counter>=0:
        if UPS[delete_counter]==0:
            UPS = np.delete(UPS, delete_counter)
        delete_counter -= 1

    delete_counter = len(DNS)-1
    while delete_counter >=0:
        if DNS[delete_counter] == 0:
            DNS = np.delete(DNS, delete_counter)
        delete_counter-=1

    #computing EMA
    EMA_counter = 1
    while EMA_counter<len(UPS):
        EMA_up=EMAcalc_for_RSI(rad,UPS[EMA_counter],EMA_up)
        EMA_counter += 1

    EMA_counter = 1
    while EMA_counter<len(DNS):
        EMA_down=EMAcalc_for_RSI(rad,DNS[EMA_counter],EMA_down)
        EMA_counter += 1

    avg_up=EMA_up
    avg_down=EMA_down
    RS=avg_up/avg_down
    RS_index=100-100/(1+RS)

    return RS_index



def SMMAcalc_for_RSI(days, gain,prev_avg):
    #fx=1/days
    #EMA=fx*(price-prev_avg)+prev_avg
    EMA = (prev_avg * (days - 1) + gain)/days
    return EMA



def RSI_SMMA(df,n,colprice, rad):#with simple moving avg. for EMA, change after the while
    import numpy as np

    upcounter=0
    downcounter=0
    upsum=0
    downsum=0
    n_count=n+rad-1
    i=0
    j=0

    UPS=np.zeros(rad)
    DNS=np.zeros(rad)

    while n_count>=n:
        if df.iloc[n_count, colprice]>df.iloc[n_count+1, colprice]:#up
            UPS[i]=abs(df.iloc[n_count,colprice]-df.iloc[n_count+1,colprice])
            if upcounter==0:
                EMA_up=abs(df.iloc[n_count,colprice]-df.iloc[n_count+1,colprice])
            i+=1
            upcounter += 1

        elif df.iloc[n_count, colprice]<df.iloc[n_count-1, colprice]:
            DNS[j] = abs(df.iloc[n_count, colprice] - df.iloc[n_count + 1, colprice])
            if downcounter==0:
                EMA_down=abs(df.iloc[n_count,colprice]-df.iloc[n_count+1,colprice])
            downcounter += 1
            j+=1

        n_count=n_count-1

    #deleting 0 values:
    delete_counter=len(UPS)-1
    while delete_counter>=0:
        if UPS[delete_counter]==0:
            UPS = np.delete(UPS, delete_counter)
        delete_counter -= 1

    delete_counter = len(DNS)-1
    while delete_counter >=0:
        if DNS[delete_counter] == 0:
            DNS = np.delete(DNS, delete_counter)
        delete_counter-=1

    try:
        EMA_down=DNS[0]#np.sum(DNS)/rad #for first one
    except:
        EMA_down = 0

    try:
        EMA_up = UPS[0]  # np.sum(UPS)/rad #for first one
    except:
        EMA_up = 0  # np.sum(UPS)/rad #for first one

    #computing SMMA
    EMA_counter = 1
    while EMA_counter<len(UPS):
        EMA_up=SMMAcalc_for_RSI(rad,UPS[EMA_counter],EMA_up)
        EMA_counter += 1

    EMA_counter = 1
    while EMA_counter<len(DNS):
        EMA_down=SMMAcalc_for_RSI(rad,DNS[EMA_counter],EMA_down)
        EMA_counter += 1



    RS=EMA_up/EMA_down
    RS_index=100-100/(1+RS)

    return RS_index




def buy_conditions_RSI_stoch(df,n):
    RSI=df.iloc[n,12]
    STOCH=df.iloc[n,16]
    if RSI<30 and STOCH<20:
        return True
    else:
        return False

def sell_conditions_RSI_stoch(df,n, stp):
    RSI = df.iloc[n,12]
    STOCH=df.iloc[n,16]
    if RSI>70 and STOCH>80:
       return True
    #if df.iloc[n,4]<stp:
    #    return True
    else:
        return False

def buy_conditions_RSI_stoch(df,n):
    RSI=df.iloc[n,1]
    STOCH=df.iloc[n,5]
    if RSI<30 and STOCH<20:
        return True
    else:
        return False

def sell_conditions_RSI_stoch(df,n, stp):
    RSI = df.iloc[n,1]
    STOCH=df.iloc[n,5]
    if RSI>70 and STOCH>80:
       return True
    #if df.iloc[n,4]<stp:
    #    return True
    else:
        return False

def buy_conditions_EMA_f(df,n):
    EMA8=df.iloc[n,3]
    EMA13 = df.iloc[n, 4]
    EMA21 = df.iloc[n, 5]
    EMA55 = df.iloc[n, 6]
    if EMA8>EMA13 and EMA13>EMA21 and EMA21>EMA55:
        return True
    else:
        return False

def sell_conditions_EMA_f(df,n):
    EMA8=df.iloc[n,3]
    EMA13 = df.iloc[n, 4]
    EMA21 = df.iloc[n, 5]
    EMA55 = df.iloc[n, 6]
    if not (EMA8>EMA13 and EMA13>EMA21 and EMA21>EMA55):
       return True
    else:
        return False




