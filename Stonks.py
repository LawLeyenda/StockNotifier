from iexfinance.stocks import Stock
import os
import Passwords
import numpy as np
import pandas as pd
import datetime
import threading
import AutomateEmail
import StockData

os.environ['IEX_TOKEN'] = Passwords.IEX_TOKEN


class Stonks:

    def __init__(self, stockData):
        self.myStockData = stockData

    def price(self, ticker):
        try:
            price = float(Stock(ticker).get_price())
            self.myStockData.at["price", ticker] = price
        except:
            try:
                price = float(Stock(ticker).get_close())
                self.myStockData.at["price", ticker] = price
            except:
                self.myStockData.at["price", ticker] = 0.0

    """ returns price of stock. if the market is closed it returns the market close. 
    If the market is open, it returns the current price. Must use quotes with ticker """

    def update_stock(self, ticker):
        ticker = ticker.upper()
        stock_quote = Stock(ticker).get_quote()
        self.myStockData.at["price", ticker] = stock_quote.get('latestPrice')
        self.myStockData.at["yesterday_close", ticker] = stock_quote.get('previousClose')
        self.myStockData.at['company_name', ticker] = stock_quote.get('companyName')
        self.myStockData.at["pe_ratio", ticker] = stock_quote.get('pe_ratio')
        self.myStockData.at["week52High", ticker] = stock_quote.get('week52High')
        self.myStockData.at["week52Low", ticker] = stock_quote.get('week52Low')

    def add_stock(self, ticker):
        ticker = ticker.upper()
        stock_quote = Stock(ticker).get_quote()
        self.myStockData[ticker] = ""
        self.myStockData.at["price", ticker] = stock_quote.get('latestPrice')
        self.myStockData.at["yesterday_close", ticker] = stock_quote.get('previousClose')
        self.myStockData.at['company_name', ticker] = stock_quote.get('companyName')
        self.myStockData.at["pe_ratio", ticker] = stock_quote.get('pe_ratio')
        self.myStockData.at["week52High", ticker] = stock_quote.get('week52High')
        self.myStockData.at["week52Low", ticker] = stock_quote.get('week52Low')

    '''add stock'''

    def previous_day(self):
        for stock in self.myStockData:
            self.myStockData.at["yesterday_close", stock] = float(Stock(stock).get_previous_day_prices().get('close'))

    '''get yesterday closing price of stocks from stock list'''

    def notify_user(self, ticker):
        price = self.myStockData.at['price', ticker]
        numerator = price - self.myStockData.at['yesterday_close', ticker]
        change = round(numerator / self.myStockData.at['yesterday_close', ticker] * 100, 2)
        if self.myStockData.at['user_notified?', ticker] != 1:  # remember to reset to 0 at the end of a trading day
            if change >= 2.5 or change <= -2.5:
                self.myStockData.at[
                    'user_notified?', ticker] = 1  # set notification to true for further notification constraints
                self.myStockData.at['user_notified_price', ticker] = price
                self.myStockData.at['user_notified_time', ticker] = datetime.datetime.now()
                self.myStockData.at['user_notified_percent', ticker] = change
                email_subject = self.myStockData.at['company_name', ticker]
                # change message based on increase or decrease
                if change > 0:
                    changed = "increased"
                else:
                    changed = "decreased"
                email_body = email_subject + f" has {changed} by " + str(round(change, 2)) + "% and is currently trading at $" + str(price) + "."
                AutomateEmail.automaticEmail(email_subject, email_body)  # sends email notifier user of change

    """ notifies user of price of stock is change is greater than 2.5% """

    def renotify(self, ticker):
        if self.myStockData.at['user_notified?', ticker] == 1:
            price = self.myStockData.at['price', ticker]
            numerator = price - self.myStockData.at['yesterday_close', ticker]
            change = round(numerator / self.myStockData.at['yesterday_close', ticker] * 100, 2)

            if (self.myStockData.at['user_notified_percent', ticker] > 0 and change >= 1) or (self.myStockData.at[
                                                                                                  'user_notified_percent', ticker] < 0 and change <= -1):  # if the the notified change is positive
                email_subject = self.myStockData.at['company_name', ticker] + "," + str(price)
                if change > 0:
                    changed = "increased"
                    news = "Good news!"
                else:
                    changed = "decreased"
                    news = "Bad news!"
                email_body = f"{news} " + email_subject + f" has {changed} by " + str(change - self.myStockData.at[
                    'user_notified_percent', ticker]) + "% and is currently trading at $" + str(price) + "."
                AutomateEmail.automaticEmail(email_subject, email_body)
                self.myStockData.at['user_notified_price', ticker] = price
                self.myStockData.at['user_notified_time', ticker] = datetime.datetime.now()
                self.myStockData.at['user_notified_percent', ticker] = change

    def update_prices(self):
        # update prices during stock market times
        # threading.Timer(30.0, Stonks.update_prices).start()
        for stock in self.myStockData:
            self.price(stock)
            self.notify_user(stock)
            self.renotify(stock)
        StockData.save(self.myStockData, "myStockData.csv")
