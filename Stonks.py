from iexfinance.stocks import Stock
import os
import Passwords
import numpy as np
import datetime
import threading
import AutomateEmail

os.environ['IEX_TOKEN'] = Passwords.IEX_TOKEN

''' - test cost 
my_stock_list = {'GM', 'XOM', 'OVV', 'TSLA', 'AAPL', 'MMM', 'COST', 'WMT', 'SHOP','T' }
for stock in my_stock_list:
    Stonks.price(stock)
    
Stonks.previous_day()

Stonks.add_stock("CMG")
'''
class Stonks:
    stock_list = {}
    stock_list_yesterday = {}
    #close price of yesterdays stocks

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
    def add_stock(ticker):
        Stonks.stock_list_yesterday[ticker] = float(Stock(ticker).get_previous_day_prices().get('close'))
        Stonks.price(ticker)
    '''add stock'''

    @staticmethod
    def previous_day():
        for stock in Stonks.stock_list:
            Stonks.stock_list_yesterday[stock] = float(Stock(stock).get_previous_day_prices().get('close'))
    '''get yesterday closing price of stocks from stock list'''

    @staticmethod
    def price_change(ticker):
        numerator = float(Stonks.price(ticker)) - Stonks.stock_list_yesterday.get(ticker)
        change = round(numerator / Stonks.stock_list_yesterday.get(ticker) * 100, 2)
        # test variable
        if change >= 2.5 or change <= -2.5:
            Stonks.stock_user_notified_price[ticker] = Stonks.price(ticker)
            Stonks.stock_user_notified_timer[ticker] = datetime.datetime.now()
            Stonks.stock_user_notified_percent[ticker] = change
            # add to notified dict
            email_subject = Stock(ticker).get_company_name()
            #change message based on increase or decrease
            if change > 0:
                changed = "increased"
            else:
                changed = "decreased"
            email_body = email_subject + f" has {changed} by " + str(
                round(change, 2)) + "% and is currently trading at $" + str(Stonks.price(ticker)) + "."
            AutomateEmail.automaticEmail(email_subject, email_body)
    """ notifies user of price of stock is change is greater than 2.5% """

    ### possibly add option based on volatility

    @staticmethod
    def renotify(ticker):
        numerator = Stonks.stock_list.get(ticker) - Stonks.stock_list_yesterday.get(ticker)
        change = numerator / Stonks.stock_list_yesterday.get(ticker)

        notified = float(Stonks.stock_user_notified_price.get(ticker))
        new = float(Stonks.stock_list.get(ticker))

        numerator_notified = new - notified

        change_since_notified = (numerator_notified / notified) * 100
        difference = datetime.datetime.now() - Stonks.stock_user_notified_timer.get(ticker)

        first = (change_since_notified - float(Stonks.stock_user_notified_percent.get(ticker))) > 2
        first_part2 = (change_since_notified - float(Stonks.stock_user_notified_percent.get(ticker))) < -2
        # if change is greater than or less than 2%
        second = (change_since_notified - float(Stonks.stock_user_notified_percent.get(ticker))) > .1
        second_part2 = (float(change_since_notified - Stonks.stock_user_notified_percent.get(ticker))) < -1
        # change is greater than or less than 1%
        second_part3 = ((difference.seconds / 3600) > 60)
        # difference is greater than 60 minutes

        if (first or first_part2) or ((second or second_part2) and second_part3):
            Stonks.stock_user_notified_price[ticker] = float(Stock(ticker).get_price())
            Stonks.stock_user_notified_price[ticker] = datetime.datetime.now()
            Stonks.stock_user_notified_percent[ticker] = change
            # add to notified dict
            email_subject = "Notice " + str(Stock(ticker).get_company_name())
            if change > 0:
                changed = "increased"
            else:
                changed = "decreased"
            email_body = email_subject + f" has {changed} by an additional " + str(round(
                change_since_notified, 2)) + "% and is currently " \
                                                   "trading at $" + str(Stonks.stock_list.get(ticker)) + "."

            AutomateEmail.automaticEmail(email_subject, email_body)

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
