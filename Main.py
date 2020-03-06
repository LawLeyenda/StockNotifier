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


def main():
    print("Starting...")
    data = StockData.read('myStockData.csv')
    stock_system = Stocks.Stocks(data)
    email = AutomateEmail.AutomateEmail()

    for stock in stock_system.myStockData:
        stock_system.update_add_stock(stock)
        # none then email.renotify() does not need to run

    def automation():
        print("started")
        stock_system.update_prices(email)  # calls automate email

    def end_of_day():
        print("end_of_day")
        stock_system.end_of_day()
        print("end_of_day - method called ")# time based on datetime

    def end_of_week():
        print("end_of_week")
        stock_system.end_of_week()

    def run_threaded(job_func):
        job_thread = threading.Thread(target=job_func)
        job_thread.start()  # multi thread

    schedule.every(30).seconds.do(run_threaded, automation) #time based on datetime
    schedule.every(30).seconds.do(run_threaded, end_of_day) #time based on datetime
    schedule.every().minute.do(run_threaded, end_of_week)#time based on datetime

    while 1:
        schedule.run_pending()
        time.sleep(1)


main()
