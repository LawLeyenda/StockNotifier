import news
import stocks
import AutomateEmail
import StockData
from Db import Db


def main_minitest():
    print("Starting...")
    data = StockData.read('myStockData.csv')
    stock_system = stocks.Stocks(data)
    db_test = Db('stock.db')
    # x = ("AAPL", "4333434535", "Test", "2322","234242")
    # y = ("AAPL", "433334335343", "Test1", "2322","234242")
    # db_test.sql_insert_stock_news(x)
    # db_test.sql_insert_stock_news(y)
    print(db_test.sql_fetch_many("*", "StockNews WHERE stock_name = \"AAPL\""))
    print(db_test.sql_fetch_one("*", "Stock WHERE stock_name = \"T\""))


    # email = AutomateEmail.AutomateEmail()

    # my_news = news.News(stock_system)
    # print(my_news.myStockData)
    # my_news.myStockData.at["price", "AAPL"] = 300
    # print(id(stock_system.myStockData))
    # print(id(my_news.myStockData))
    # stock_system.myStockData.at["price", "AAPL"] = 400
    # print(my_news.myStockData)

    # stock_system.myStockData.at['price', 'AAPL'] = 300
    # print(stock_system.myStockData)


main_minitest()
