from iexfinance.stocks import Stock
import re
import datetime
# every stock creates its over news object
# retrieve news about stocks.
class All_News:

    def __init__(self, Stocks): #sets current stockdata to the same reference as Stocks class "myStockData"
        self.myStockData = Stocks.myStockData


class stock_news:

    def daily_news(ticker, db):
        pass

    @staticmethod
    def notify_news(ticker, db): #returns the 3 most recent articles if all articles have been used.
        three_news_articles = []
        news_list = db.sql_fetch_many("Article,url,summary,article_used", "StockNews where stock_name = \"%s\" order by datetime desc" % ticker)
        if news_list is not None:
            for x in news_list:
                if x[3] == 0 and (len(three_news_articles) < 3):
                    three_news_articles.append(x)
                    db.sql_update_open("StockNews", "article_used = 1 where url = \"%s\"" % (x[1])) # i dont think this makes sense!
            for x in news_list: # seems like really inefficient code
                if len(three_news_articles) < 3:
                    three_news_articles.append(x)
            return three_news_articles
        return None

    @staticmethod
    def query_news(ticker, db): #gets news
        stock_news = Stock(ticker).get_news()
        for news in stock_news:
            date = news.get('datetime')
            date = datetime.datetime.fromtimestamp(date / 1e3)
            headline = news.get('headline')
            summary = news.get('summary')
            url = news.get('url')
            # company_name = Stock(ticker).get_company_name()
            values = (ticker, 0 , headline, url, date, summary)
            db.sql_insert_stock_news(values)

    def news(self, ticker, db): #collate the three news articles
        my_news = self.notify_news(ticker, db)
        news_string = ""
        for news in my_news:
            news_string = news_string + "\n----------------------------------" + "\n\n\n" + str(news[0]) + "\n\n" + str(news[2]) + "\n\n" + str(news[1]) \
                          + "\n"
        return news_string



    def clarify(self, ticker):
        pass