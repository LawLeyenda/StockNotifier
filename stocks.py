from iexfinance.stocks import Stock
import os
import Passwords
from datetime import datetime, timedelta
import news
import StockData

os.environ['IEX_TOKEN'] = Passwords.IEX_TOKEN


class Stocks:

    def __init__(self, stock_data):
        self.myStockData = stock_data
        # my_news = news.News(self.myStockData) #creates my_news object that uses info from myStockData

    # @property
    # def myStockData(self):
    #     return self.myStockData
    #@myStockData.setter



    def price(self, ticker):
        try:
            # price = float(Stock(ticker).get_price())
            price = Stock(ticker).get_price()

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
        if ticker not in self.myStockData:
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
        name = self.myStockData.at['company_name', ticker]
        change = round(numerator / self.myStockData.at['yesterday_close', ticker] * 100, 2)  # change is as 1s digit
        if self.myStockData.at['user_notified?', ticker] != 1:  # remember to reset to 0 at the end of a trading day
            if change >= 2.5 or change <= -2.5:
                self.myStockData.at[
                    'user_notified?', ticker] = 1  # set notification to true for further notification constraints
                self.myStockData.at['user_notified_price', ticker] = price
                time_now = datetime.now()

                self.myStockData.at['user_notified_time', ticker] = time_now - timedelta(hours=5)
                self.myStockData.at['user_notified_percent', ticker] = change
                return [ticker, name, price, change]  # send out email

    """ notifies user of price of stock is change is greater than 1.5% """

    def renotify(self, ticker):
        if self.myStockData.at['user_notified?', ticker] == 1:
            price = self.myStockData.at['price', ticker]
            notified = self.myStockData.at['user_notified_percent', ticker]
            numerator = price - self.myStockData.at['yesterday_close', ticker]
            name = self.myStockData.at['company_name', ticker]
            change = round((numerator / self.myStockData.at['yesterday_close', ticker]) * 100, 2)
            time_now = datetime.now()
            if (notified > 0 and change >= 1.5 + notified) or \
                    (notified < 0 and change <= -1.5 + notified) and \
                    (int((time_now - self.myStockData.at[
                        'user_notified_time', ticker]).total_seconds()) > 3600):  # if the the notified change is greater than 1.5 and the time has been creater than an hour
                self.myStockData.at['user_notified_price', ticker] = price
                self.myStockData.at['user_notified_time', ticker] = time_now - timedelta(hours=5)
                self.myStockData.at['user_notified_percent', ticker] = change
                return [ticker, name, price, change]  # send out email

    def update_prices(self, email):
        #print("updating...")
        # calls email object and sends out email if notifications hit threshold
        for stock in self.myStockData:
            self.price(stock)
            temp = self.notify_user(stock)
            email.notify(temp)
            temp = self.renotify(stock)
            email.renotify_email(temp)
            StockData.save(self.myStockData, "myStockData.csv")
            # time.sleep(30)  # run every 30 seconds -- currently processed in main

    def end_of_day(self):
            # house keeping
            # reset user_notified to 0
        print("end of day running")
        for stock in self.myStockData:
            self.myStockData.at['user_notified?', stock] = 0
            self.myStockData.at['user_notified_percent', stock] = 0
            self.myStockData.at['user_notified_price', stock] = 0
            self.myStockData.at['user_notified_time', stock] = 0
            StockData.save(self.myStockData, "myStockData.csv")

    def end_of_week(self):  # eventually add weekly report
        time_now = datetime.now()
        if time_now.hour == 21 and (time_now.minute == 1 or time_now.minute == 2) and time_now.day == 6:
            print("end of week running")
            # update price_targets for analysts
            for stock in self.myStockData:
                retrieve_data = Stock(stock).get_price_target()  # get analysis data
                self.myStockData.at['priceTargetAverage', stock] = retrieve_data.get('priceTargetAverage')
                self.myStockData.at['numberOfAnalysts', stock] = retrieve_data.get('numberOfAnalysts')
                StockData.save(self.myStockData, "myStockData.csv")
