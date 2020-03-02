import Passwords
import Stonks
import threading
import datetime
import schedule
import time
import AutomateEmail

def main():
    my_stock_list = {'GM', 'XOM', 'OVV', 'TSLA', 'AAPL', 'MMM'}
    test = Stonks.Stonks()
    for stock in my_stock_list:
        test.price(stock)

    schedule.every().day.at("09:30").do(test.update_prices())



main()

