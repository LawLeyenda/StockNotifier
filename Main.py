import schedule
import time
import Stonks
import AutomateEmail
import Passwords


def main():
    my_stock_list = {'GM', 'XOM', 'OVV', 'TSLA', 'AAPL', 'MMM'}
    print("Starting...")
    test = Stonks.Stonks()

    for stock in my_stock_list:
    test.price(stock)

    def job():
        print("started...")
        test.update_prices()
        #AutomateEmail.automaticEmail("does this work", "on the server ")

    schedule.every().day.do(job)
    
    '''schedule.every().day.at("09:30").do()'''

    while 1:
        schedule.run_pending()
        time.sleep(1)




main()
