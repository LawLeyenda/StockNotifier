import news
import stocks
import AutomateEmail
import StockData


def main_minitest():
    print("Starting...")
    data = StockData.read('myStockData.csv')
    stock_system = stocks.Stocks(data)
    # email = AutomateEmail.AutomateEmail()

    my_news = news.News(stock_system)
    print(my_news.myStockData)
    my_news.myStockData.at["price", "AAPL"] = 300
    print(id(stock_system.myStockData))
    print(id(my_news.myStockData))
    stock_system.myStockData.at["price", "AAPL"] = 400
    print(my_news.myStockData)

    # stock_system.myStockData.at['price', 'AAPL'] = 300
    # print(stock_system.myStockData)


main_minitest()
