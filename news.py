from iexfinance.stocks import Stock


# every stock creates its over news object
# retrieve news about stocks.
class All_News:

    def __init__(self, Stocks): #sets current stockdata to the same reference as Stocks class "myStockData"
        self.myStockData = Stocks.myStockData


class Stock_News:

    def daily(self):
        pass

    def notify_news(self, ticker):
        pass

    def query_news(self, ticker): #gets news
        stock_news = Stock(ticker).get_news()



    def clarify(self, ticker):
        pass