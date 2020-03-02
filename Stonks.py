from iexfinance.stocks import Stock
import os
import Passwords
import numpy as np
import datetime
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
        numerator = float(Stonks.price(ticker)) - float(Stock(ticker).get_close())
        change = round(numerator / Stock(ticker).get_close() * 100, 2)
        # test variable
        if change >= .025:
            Stonks.stock_user_notified_price[ticker] = Stonks.price(ticker)
            Stonks.stock_user_notified_timer[ticker] = datetime.datetime.now()
            Stonks.stock_user_notified_percent[ticker] = change
            # add to notified dict
            email_subject = Stock(ticker).get_company_name()
            email_body = email_subject + " has increased by " + str(
                round(change * 100, 2)) + "% and is currently trading at $" + str(Stonks.price(ticker)) + "."
            AutomateEmail.automaticEmail(email_subject, email_body)

        if change <= -.025:
            Stonks.stock_user_notified_price[ticker] = Stonks.price(ticker)
            Stonks.stock_user_notified_timer[ticker] = datetime.datetime.now()
            Stonks.stock_user_notified_percent[ticker] = change
            # add to notified dict
            email_subject = Stock(ticker).get_company_name()
            email_body = email_subject + " has decreased by " + str(
                round(change * 100, 2)) + "% and is currently trading at $" + str(Stonks.price(ticker)) + "."
            AutomateEmail.automaticEmail(email_subject, email_body)

    """ notifies user of price of stock is change is greater than 2.5% """

    ### possibly add option based on volatility

    @staticmethod
    def renotify(ticker):
        numerator = Stonks.price(ticker) - float(Stock(ticker).get_close())
        change = numerator / Stock(ticker).get_close()

        notified = float(Stonks.stock_user_notified_price.get(ticker))
        new = float(Stonks.price(ticker))

        numerator_notified = new - notified

        change_since_notified = numerator_notified / notified
        difference = datetime.datetime.now() - Stonks.stock_user_notified_timer.get(ticker)

        first = (change_since_notified - float(Stonks.stock_user_notified_percent.get(ticker))) > .02
        first_part2 = (change_since_notified - float(Stonks.stock_user_notified_percent.get(ticker))) < -.02
        # if change is greater than or less than 2%
        second = (change_since_notified - float(Stonks.stock_user_notified_percent.get(ticker))) > .01
        second_part2 = (float(change_since_notified - Stonks.stock_user_notified_percent.get(ticker))) < -.01
        # change is greater than or less than 1%
        second_part3 = ((difference.seconds / 3600) > 60)
        # difference is greater than 60 minutes

        if (first or first_part2) or ((second or second_part2) and second_part3):
            Stonks.stock_user_notified_price[ticker] = float(Stock(ticker).get_price())
            Stonks.stock_user_notified_price[ticker] = datetime.datetime.now()
            Stonks.stock_user_notified_percent[ticker] = change
            # add to notified dict
            email_subject = Stock(ticker).get_company_name()
            email_body = email_subject + " has changed by an additional " + str(round(
                change_since_notified * 100, 2)) + "% and is currently " \
                                                   "trading at $" + str(Stonks.price(ticker)) + "."

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
