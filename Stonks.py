from iexfinance.stocks import Stock
import os
import Passwords
import numpy as np
from datetime import datetime, date, time, timedelta
import threading
import AutomateEmail

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
            a = Stonks.stock_user_notified_price[ticker] = Stonks.price(ticker)
            b = Stonks.stock_user_notified_timer[ticker] = datetime.datetime.now()
            c = Stonks.stock_user_notified_percent[ticker] = change
            # add to notified dict
            email_subject = Stock(ticker).get_company_name()
            email_body = email_subject + " has increased by " + str(
                round(change * 100, 2)) + "% and is currently trading at $" + str(Stonks.price(ticker)) + "."
            AutomateEmail.automaticEmail(email_subject, email_body)
            return a,b,c

        if change <= -.025:
            a = Stonks.stock_user_notified_price[ticker] = Stonks.price(ticker)
            b = Stonks.stock_user_notified_timer[ticker] = datetime.datetime.now()
            c = Stonks.stock_user_notified_percent[ticker] = change
            # add to notified dict
            email_subject = Stock(ticker).get_company_name()
            email_body = email_subject + " has decreased by " + str(
                round(change * 100, 2)) + "% and is currently trading at $" + str(Stonks.price(ticker)) + "."
            AutomateEmail.automaticEmail(email_subject, email_body)
            return a, b, c

    """ notifies user of price of stock is change is greater than 2.5% """

    ### possibly add option based on volatility

    @staticmethod
    def renotify(ticker):
        numerator = np.subtract(Stonks.price(ticker), float(Stock(ticker).get_close()))
        change = np.divide(numerator, Stock(ticker).get_close())

        notified = float(Stonks.stock_user_notified_price.get(ticker))
        new = float(Stonks.price(ticker))

        numerator_notified = np.subtract(new, notified)

        change_since_notified = np.divide(numerator_notified, notified)
        a = Stonks.stock_user_notified_timer.get(ticker)
        difference = datetime.datetime.now() - a
        if ((
                change_since_notified - Stonks.stock_user_notified_percent.get(ticker) > .02 | change_since_notified - Stonks.stock_user_notified_percent.get(ticker) < -.02)
                | ((
                           change_since_notified - Stonks.stock_user_notified_percent.get(ticker) > .01 | change_since_notified - Stonks.stock_user_notified_percent.get(ticker) < -.01)
                   & (difference.seconds/3600) > 60)):
            Stonks.stock_user_notified_price[ticker] = float(Stock(ticker).get_price())
            Stonks.stock_user_notified_price[ticker] = datetime.datetime.now()
            Stonks.stock_user_notified_percent[ticker] = change
            # add to notified dict
            email_body = str(Stock(ticker).get_company_name()) + " has changed by an additional" + str(
                change_since_notified) + "% and is currently " \
                                         "trading at $" + str(round(change * 100, 2)) + "."

    """ updates the user on the price of the stock if stock is +/- an additional 1% of notified price after 1 hour. 
    If stock is +/- additional 2%, notifies the user immediately"""

    @staticmethod
    def update_prices():
        # update prices during stock market times
        threading.Timer(30.0, Stonks.update_prices).start()
        for stock in Stonks.stock_list:
            Stonks.price_change(stock)

        for stock in Stonks.stock_user_notified_price:
            Stonks.renotify(stock)
