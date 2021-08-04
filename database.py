import sqlite3
from parameters import *
from datetime import datetime, timezone

def create():
    """create database if it doesn\'t exist"""
    con = sqlite3.connect('../crypto.db')
    cur = con.cursor()
    query=f"""CREATE TABLE IF NOT EXISTS {symbol()} (timestamp, price, short_ma, long_ma, money, action)"""
    cur.execute(query)
    con.commit()
    con.close()

def add_row_to_db(price,long,short, money, action):
    """Add a row to the database.
    
    Args:
        price (float): price of the pair.
        long (int): price of long avg.
        short (int): price of short avg.
        money (float): money available in account for the two pairs.
        action (str): "BUY" , "SELL" or "-"
    """
    con = sqlite3.connect('../crypto.db')
    cur = con.cursor()
    now=datetime.now()
    timestamp = datetime.timestamp(now)
    query=f"INSERT INTO {symbol()} VALUES (?,?,?,?,?,?)"
    cur.execute(query,(timestamp ,price, long, short, money, action))
    con.commit()
    con.close()

def check_table():
    query=f"SELECT * FROM {symbol()} ORDER BY timestamp"
    con = sqlite3.connect('../crypto.db')
    cur = con.cursor()
    cur.execute(query)
    for row in cur.fetchall():
        print(row)
    con.commit()
    con.close()



if __name__=="__main__":
    #create()
    #add_row_to_db(10,33,43,23,"SELL")
    check_table()

