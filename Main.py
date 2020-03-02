import os
import passwords
os.environ['IEX_TOKEN'] = passwords.IEX_TOKEN

from iexfinance.stocks import Stock


def price(ticker):
    try:
        return Stock(ticker).get_price()
    except:
        try:
            return Stock(ticker).get_close()
        except:
            return 0.0
"""returns price of stock. if the market is closed it returns the market close. 
If the market is open, it returns the current price. Must use quotes with ticker """

