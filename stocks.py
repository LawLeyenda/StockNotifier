from iexfinance.stocks import Stock
import os
import Passwords
from datetime import datetime, timedelta

import news
import StockData
from Db import Db

os.environ['IEX_TOKEN'] = Passwords.IEX_TOKEN


class Stocks:

    # def __init__(self, database):
    #     self.myDataBase = database
    # my_news = news.News(self.myStockData) #creates my_news object that uses info from myStockData

    # my_news = news.News(self.myStockData) #creates my_news object that uses info from myStockData

    # @property
    # def myStockData(self):
    #     return self.myStockData
    # @myStockData.setter
    def price_fetch_price(self, ticker, price, database):  # sub method of price
        if database.sql_fetch_one("*", "Stock where stock_name = \"%s\"" % ticker) is None:
            # if none then call update_add_stock function
            self.update_add_stock(self, ticker, database)
        else:
            database.sql_update_open("Stock", "price = %s WHERE stock_name = \"%s\"" % (price, ticker))

    def price(self, ticker, database):
        try:
            # price = float(Stock(ticker).get_price())
            price = Stock(ticker).get_price()

            # self.myDatabase.at["price", ticker] = price
            self.price_fetch_price(ticker, price, database)
        except:
            try:
                price = float(Stock(ticker).get_close())
                # self.myDatabase.at["price", ticker] = price
                self.price_fetch_price(ticker, price, database)
            except:
                price = 0.0
                self.price_fetch_price(ticker, price, database)

    """ returns price of stock. if the market is closed it returns the market close. 
    If the market is open, it returns the current price. Must use quotes with ticker """

    def update_add_stock(self, ticker, database):
        ticker = ticker.upper()
        stock_quote = Stock(ticker).get_quote()
        if database.sql_fetch_one("*", "Stock where stock_name = \"%s\"" % ticker) is None:
            entities = (
                ticker, stock_quote.get('companyName'), stock_quote.get('latestPrice'),
                stock_quote.get('previousClose'),
                stock_quote.get('peRatio'), stock_quote.get('week52High'), stock_quote.get('week52Low'))
            database.sql_insert_stock(entities)
        else:
            entities = (
                ticker, stock_quote.get('companyName'), stock_quote.get('latestPrice'),
                stock_quote.get('previousClose'),
                stock_quote.get('peRatio'), stock_quote.get('week52High'), stock_quote.get('week52Low'), ticker)
            database.sql_update(entities)

        if database.sql_fetch_one("stock_name", "UserNotified where stock_name = \"%s\"" % ticker) is None:
            entities = (None, None, None, None, None, ticker, None)
            database.sql_insert_user_notified(entities)

    '''add stock/update'''

    @staticmethod
    def delete_stock(ticker, database):
        database.sql_delete_stock("\"%s\"" % ticker)

    def previous_day(self):
        for stock in self.myDatabase:
            self.myDatabase.at["yesterday_close", stock] = float(Stock(stock).get_previous_day_prices().get('close'))

    '''get yesterday closing price of stocks from stock list'''

    def notify_user(self, ticker, database):
        yesterdays_close = database.sql_fetch_one("yesterday_close", "Stock where stock_name = \"%s\"" % ticker)
        price = database.sql_fetch_one("price", "Stock where stock_name = \"%s\"" % ticker)
        numerator = price - yesterdays_close
        name = database.sql_fetch_one("company_name", "Stock where stock_name = \"%s\"" % ticker)
        change = round(numerator / yesterdays_close * 100, 2)  # change is as 1s digit
        if database.sql_fetch_one("is_user_notified",
                                  "UserNotified where stock_name = \"%s\"" % ticker) != 1:  # remember to reset to 0 at the end of a trading day
            if change >= 2.5 or change <= -2.5:
                database.sql_update_open("UserNotified",
                                         "is_user_notified = \"%s\" where stock_name = \"%s\"" % (1, ticker))
                # set notification to true for further notification constraints
                database.sql_update_open("UserNotified",
                                         "notified_price = %s where stock_name = \"%s\"" % (price, ticker))
                time_now = datetime.now()
                # import datetime and update later
                database.sql_update_open("UserNotified",
                                         "notified_time = \"%s\" where stock_name = \"%s\"" % (time_now, ticker))
                # self.myDatabase.at['user_notified_time', ticker] = time_now - timedelta(hours=5)
                database.sql_update_open("UserNotified",
                                         "notified_percent = \"%s\" where stock_name = \"%s\"" % (change, ticker))
                return [ticker, name, price, change]  # send out email

    """ notifies user of price of stock is change is greater than 1.5% """

    @staticmethod
    def renotify(ticker, database):
        if database.sql_fetch_one("is_user_notified", "UserNotified where stock_name = \"%s\"" % ticker) == 1:
            price = database.sql_fetch_one("price", "Stock where stock_name = \"%s\"" % ticker)
            notified = database.sql_fetch_one("notified_percent", "UserNotified where stock_name = \"%s\"" % ticker)
            yesterdays_close = database.sql_fetch_one("yesterday_close", "Stock where stock_name = \"%s\"" % ticker)
            numerator = price - yesterdays_close
            name = database.sql_fetch_one("company_name", "Stock where stock_name = \"%s\"" % ticker)
            change = round((numerator / yesterdays_close * 100), 2)
            time_now = datetime.now()
            notified_time = database.sql_fetch_one("notified_time", "UserNotified where stock_name = \"%s\"" % ticker)
            if (notified > 0 and change >= 1.5 + notified) or \
                    (notified < 0 and change <= -1.5 + notified) and \
                    (int((
                                 time_now - notified_time).total_seconds()) > 3600):  # if the the notified change is greater than 1.5 and the time has been creater than an hour
                database.sql_update_open("UserNotified",
                                         "notified_price = %s where stock_name = \"%s\"" % (price, ticker))
                # self.myDatabase.at['user_notified_time', ticker] = time_now - timedelta(hours=5)
                database.sql_update_open("UserNotified",
                                         "notified_percent = %s where stock_name = \"%s\"" % (change, ticker))
                return [ticker, name, price, change]  # send out email

    def update_prices(self, email, stock_news, database):
        # print("updating...")
        # calls email object and sends out email if notifications hit threshold
        list = database.stock_list()
        for stock in list:
            self.price(stock, database)
            stock_info = self.notify_user(stock, database)
            if stock_info is not None:
                thisnews = stock_news.news(stock, database)
                email.notify(stock_info, thisnews)
            stock_info = self.renotify(stock, database) #ugly code
            if stock_info is not None:
                thisnews = stock_news.news(stock, database)
                email.renotify_email(stock_info, thisnews)
            # time.sleep(30)  # run every 30 seconds -- currently processed in main

    @staticmethod
    def end_of_day(database):
        # house keeping
        # reset user_notified to 0
        print("end of day running")
        database.sql_update_open("UserNotified",
                                 "is_user_notified = 0, notified_percent = 0, notified_time = 0, notified_price = 0")
        # for stock in self.myDatabase:
        #
        #     self.myDatabase.at['user_notified?', stock] = 0
        #     self.myDatabase.at['user_notified_percent', stock] = 0
        #     self.myDatabase.at['user_notified_price', stock] = 0
        #     self.myDatabase.at['user_notified_time', stock] = 0
        #     StockData.save(self.myDatabase, "myStockData.csv")

    def end_of_week(self, database):  # eventually add weekly report
        print("end of week running")
        # update price_targets for analysts
        count = int(database.sql_fetch_one("count(stock_name)", "Stock"))
        i = 1
        while i <= count:
            retrieve_data = Stock(stock).get_price_target()  # get analysis data
            self.myDatabase.at['priceTargetAverage', stock] = retrieve_data.get('priceTargetAverage')
            self.myDatabase.at['numberOfAnalysts', stock] = retrieve_data.get('numberOfAnalysts')
            i = i + 1
