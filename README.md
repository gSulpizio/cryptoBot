# cryptoBot

Simple bot taking a long SMA and a short EMA to buy and sell any crypto currency using the binance API.

## Setup

To set the package up, the [binance api keys](https://www.binance.com/en/support/faq/360002502072) are required. The reading and Spot & Margin trading rights are required for this bot, please don't enable any other options such as withdrawals for security reasons.

Once the api keys are known, just run [quick_start.py](./quick_start.py) to set the api keys. They are stored in the [keys.txt](./keys.txt) file. 

In order to get notifications when trades are executed, it is possible to set up your own [notify.run](https://notify.run/) server. No changes are needed other than set up the server. 

## Customization guide

To customize simple things such as the interval or the traded pair, the [constants.py](./constants.py) file can be modified. 

##### Modifying the trading pair

The trading pair can be modified 

# [Documentation](https://gsulpizio.github.io/cryptoBot)
