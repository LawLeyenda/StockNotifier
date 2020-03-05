import schedule
import time
import datetime
import Stocks
import AutomateEmail
import Passwords
import StockData
import pandas as pd
import threading
import sys

print("Starting...")
data = StockData.read('myStockData.csv')
stock_system = Stocks.Stocks(data)
email = AutomateEmail.AutomateEmail()

for stock in stock_system.myStockData:
    stock_system.update_add_stock(stock)

    # none then email.renotify() does not need to run


def automation():
    stock_system.update_prices(email)  # calls automate email
    print("started")

'''def run_threaded(job_func):
    job_thread = threading.Thread(target=job_func)
    job_thread.start()'''#multi thread


schedule.every(30).seconds.do(automation())

while 1:
    schedule.run_pending()
    time.sleep(1)
