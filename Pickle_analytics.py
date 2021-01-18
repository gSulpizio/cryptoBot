import pickle
import datetime as dt
from binance.client import Client
import pandas as pd
import numpy as np  # numerical python, i usually need this somewhere
import time as tm
import matplotlib.pyplot as plt  # for charts and such
import os
import paramiko




scores = {} # scores is an empty dict already
target='datacollection.pckl'
if os.path.getsize(target) > 0:
    with open(target, "rb") as f:
        f = open('datacollection.pckl', 'rb')
        data = pickle.load(f)
        print(data)
        #data.plot(x='date_time', y='money', color='red')
        #plt.show()
        f.close()
else:
    print('file empty :(')
'''
f = open('store.pckl', 'rb')
data = pickle.load(f)
print(data)
data.plot(x='date_time',y='money',color='red')
plt.show()
f.close()'''