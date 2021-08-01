"""writes TXT file with public and secret binance keys"""
print('Please enter public Binance api key:')
public=input()
print('Please enter public Binance api key:')
private=input()
with open('keys.txt', 'w+') as f:
    f.write(public+'\n'+private)
print("Done!")