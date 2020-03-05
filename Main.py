import schedule
import time
import Stocks
import AutomateEmail
import Passwords
import StockData
import pandas as pd

print("Starting...")
data = StockData.read('myStockData.csv')
stock_system = Stocks.Stocks(data)
email = AutomateEmail.AutomateEmail()

for stock in stock_system.myStockData:
    stock_system.update_add_stock(stock)
    # email.notify(stock_system.notify_user(stock))
    # email.renotify_email(stock_system.renotify(stock))
    # seems very inefficent and power hungry. Because if there
    # none then email.renotify() does not need to run
'''
stock_system.add_stock("MMM")
stock_system.add_stock("T")
stock_system.add_stock("schw")
stock_system.add_stock("cmg")
stock_system.add_stock("sbux")
stock_system.update_prices()';'''


def automation():
    print("started...")
    stock_system.update_prices(email)


print("running")

schedule.every(30).seconds.do(automation)

while 1:
    schedule.run_pending()
    time.sleep(1)
