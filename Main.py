import schedule
import Stonks
import AutomateEmail
import Passwords

def main():
    my_stock_list = {'GM', 'XOM', 'OVV', 'TSLA', 'AAPL', 'MMM'}
    print("Starting...")
    test = Stonks.Stonks()
    for stock in my_stock_list:
        test.price(stock)
    print("Schedule")
    schedule.every(15).seconds.do(AutomateEmail.automaticEmail("does this work", "when turned off"))

    schedule.every().day.at("09:30").do(test.update_prices())


main()
