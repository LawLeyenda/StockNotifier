import schedule
import time
import Stonks
import AutomateEmail
import Passwords


def main():
    
    my_stock_list = {'GM', 'XOM', 'OVV', 'TSLA', 'AAPL', 'MMM', 'AMZN', 'GE'}
    print("Starting...")
    test = Stonks.Stonks()

    for stock in my_stock_list:
        test.price(stock)

    test.previous_day()
    def job():
        print("started...")
        test.update_prices()
        #AutomateEmail.automaticEmail("does this work", "on the server ")

    #schedule.every(30).seconds.do(job)
    #print("running")
    #schedule.every().day.at("09:30").do(job)

    def test():
        print("Email sent!")
        AutomateEmail.automaticEmail("Script is still running", "test ")
        
    schedule.every(30).seconds.do(test)


    while 1:
        schedule.run_pending()
        time.sleep(1)


main()
