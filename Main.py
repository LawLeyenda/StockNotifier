import schedule
import time
import Stonks
import AutomateEmail
import Passwords
import StockData
import pandas as pd


print("Starting...")
data = StockData.read('myStockData.csv')
stock_system = Stonks.Stonks(data)

for stock in stock_system.myStockData:
    stock_system.update_stock(stock)


'''
stock_system.add_stock("MMM")
stock_system.add_stock("T")
stock_system.add_stock("schw")
stock_system.add_stock("cmg")
stock_system.add_stock("sbux")
stock_system.update_prices()';'''


def automation():
    print("started...")
    stock_system.update_prices()
print("running")

schedule.every(30).seconds.do(automation)



while 1:
    schedule.run_pending()
    time.sleep(1)



