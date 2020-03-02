import Passwords
import Stonks
import threading
import datetime
import schedule
import time
#import AutomateEmail

def main():
    my_stock_list = {'GM', 'XOM', 'OVV', 'TSLA'}
    schedule.every().day.at.("9:30").do(Stonks.update_prices)

    test = Stonks.Stonks()
    test.price("MSFT")

main()

