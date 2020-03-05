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


class Stocks:

    def __init__(self, stock_data):
        self.myStockData = stock_data

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

    def update_add_stock(self, ticker):
        ticker = ticker.upper()
        stock_quote = Stock(ticker).get_quote()
        if not ticker in self.myStockData:
            self.myStockData[ticker] = ""
        self.myStockData.at["price", ticker] = stock_quote.get('latestPrice')
        self.myStockData.at["yesterday_close", ticker] = stock_quote.get('previousClose')
        self.myStockData.at['company_name', ticker] = stock_quote.get('companyName')
        self.myStockData.at["pe_ratio", ticker] = stock_quote.get('peRatio')
        self.myStockData.at["week52High", ticker] = stock_quote.get('week52High')
        self.myStockData.at["week52Low", ticker] = stock_quote.get('week52Low')
        StockData.save(self.myStockData, "myStockData.csv")
    '''add stock/update'''

    def remove_stock(self, ticker):
        self.myStockData = self.myStockData.drop([ticker], axis=1)
        StockData.save(self.myStockData, "myStockData.csv")

    def previous_day(self):
        for stock in self.myStockData:
            self.myStockData.at["yesterday_close", stock] = float(Stock(stock).get_previous_day_prices().get('close'))

    '''get yesterday closing price of stocks from stock list'''

    def notify_user(self, ticker):
        price = self.myStockData.at['price', ticker]
        numerator = price - self.myStockData.at['yesterday_close', ticker]
        change = round(numerator / self.myStockData.at['yesterday_close', ticker] * 100, 2)  # change is as 1s digit
        if self.myStockData.at['user_notified?', ticker] != 1:  # remember to reset to 0 at the end of a trading day
            if change >= 2.5 or change <= -2.5:
                self.myStockData.at['user_notified?', ticker] = 1  # set notification to true for further notification constraints
                self.myStockData.at['user_notified_price', ticker] = price
                self.myStockData.at['user_notified_time', ticker] = datetime.datetime.now()
                self.myStockData.at['user_notified_percent', ticker] = change
                return [ticker, price, change]  # send out email

    """ notifies user of price of stock is change is greater than 1.5% """

    def renotify(self, ticker):
        if self.myStockData.at['user_notified?', ticker] == 1:
            price = self.myStockData.at['price', ticker]
            numerator = price - self.myStockData.at['yesterday_close', ticker]
            change = round((numerator / self.myStockData.at['yesterday_close', ticker]) * 100, 2)
            timeNow = datetime.datetime.now()
            if (self.myStockData.at['user_notified_percent', ticker] > 0 and change >= 1.5) or \
                    (self.myStockData.at['user_notified_percent', ticker] < 0 and change <= -1.5) and \
                    (int((timeNow - self.myStockData.at[
                        'user_notified_time', ticker]).total_seconds()) > 3600):  # if the the notified change is greater than 1.5 and the time has been creater than an hour
                self.myStockData.at['user_notified_price', ticker] = price
                self.myStockData.at['user_notified_time', ticker] = datetime.datetime.now()
                self.myStockData.at['user_notified_percent', ticker] = change
                return [ticker, price, change] #send out email


    def update_prices(self, email):
        for stock in self.myStockData:
            self.price(stock)
            temp = self.notify_user(stock)
            email.notify(temp)
            temp = self.renotify(stock)
            email.renotify_email(temp)
            StockData.save(self.myStockData, "myStockData.csv")

    def end_of_day(self):
        # house keeping
        # reset user_notified to 0
        for stock in self.myStockData:
            self.myStockData['user_notified?', stock] = 0
            #weekly report

    def end_of_week(self):
        # update price_targets for analysts
        for stock in self.myStockData:
            retrieve_data = Stock(stock).get_price_target() #get analysis data
            self.myStockData['priceTargetAverage', stock] = retrieve_data.get('priceTargetAverage')
            self.myStockData['numberOfAnalysts', stock] = retrieve_data.get('numberOfAnalysts')
