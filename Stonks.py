from iexfinance.stocks import Stock
import os
import Passwords
import numpy as np
import datetime
import threading
import schedule
import time

os.environ['IEX_TOKEN'] = Passwords.IEX_TOKEN


class Stonks:
    stock_list = {}
    # dict of retrieved stocks and their prices

    stock_user_notified_percent = {}
    stock_user_notified_price = {}
    stock_user_notified_timer = {}

    # dict of stocks and their prices when user was notified so they can be compared for further updates

    @staticmethod
    def price(ticker):
        try:
            price = float(Stock(ticker).get_price())
            Stonks.stock_list[ticker] = price
            return price
        except:
            try:
                price = float(Stock(ticker).get_close())
                Stonks.stock_list[ticker] = price
                return price
            except:
                return 0.0

    """ returns price of stock. if the market is closed it returns the market close. 
    If the market is open, it returns the current price. Must use quotes with ticker """

    @staticmethod
    def price_change(ticker):
        numerator = np.subtract(Stonks.price(ticker), Stock(ticker).get_close())
        change = np.divide(numerator, Stock(ticker).get_close())
        if change >= .025:
            Stonks.stock_user_notified_price[ticker] = float(Stock(ticker).get_price())
            Stonks.stock_user_notified_price[ticker] = datetime.datetime.now()
            Stonks.stock_user_notified_percent[ticker] = change
            # add to notified dict
            return str(Stock(ticker).get_company_name()) + " has increased by " + str(change) + "% and is currently " \
                                                                                                "trading at $" + str(
                Stonks.price(ticker))

        if change <= -.025:
            Stonks.stock_user_notified_price[ticker] = float(Stock(ticker).get_price())
            Stonks.stock_user_notified_price[ticker] = datetime.datetime.now()
            Stonks.stock_user_notified_percent[ticker] = change
            # add to notified dict

            return str(Stock(ticker).get_company_name()) + " has decreased by " + str(change) + "% and is currently " \
                                                                                                "trading at $" + str(
                Stonks.price(ticker))

    """ notifies user of price of stock is change is greater than 2.5% """

    ### possibly add option based on volatility

    @staticmethod
    def renotify(ticker):
        numerator = np.subtract(Stonks.price(ticker), Stock(ticker).get_close())
        change = np.divide(numerator, Stock(ticker).get_close())

        notified = Stonks.stock_user_notified_price.get(ticker)
        new = Stonks.price(ticker)

        change_since_notified = (new - notified) / notified

        difference = datetime.datetime.now() - Stonks.stock_user_notified_timer
        if ((
                change_since_notified - Stonks.stock_user_notified_percent > .02 | change_since_notified - Stonks.stock_user_notified_percent < -.02)
                | ((
                           change_since_notified - Stonks.stock_user_notified_percent > .01 | change_since_notified - Stonks.stock_user_notified_percent < -.01)
                   & difference.seconds / 3600 > 60)):
            Stonks.stock_user_notified_price[ticker] = float(Stock(ticker).get_price())
            Stonks.stock_user_notified_price[ticker] = datetime.datetime.now()
            Stonks.stock_user_notified_percent[ticker] = change
            # add to notified dict

            return str(Stock(ticker).get_company_name()) + " has changed by an additional" + str(
                change_since_notified) + "% and is currently " \
                                         "trading at $" + str(
                Stonks.price(ticker))

    """ updates the user on the price of the stock if stock is +/- an additional 1% of notified price after 1 hour. 
    If stock is +/- additional 2%, notifies the user immediately"""
    @staticmethod
    def update_prices(list):
        # run every stock to make sure they are in dict
        for stock in list:
            Stonks.price(stock)
        # update prices during stock market times
        threading.Timer(30.0, Stonks.update_prices).start()
        for stock in list:
            Stonks.price_change(stock)

        for stock in Stonks.stock_user_notified_price:
            Stonks.renotify(stock)

