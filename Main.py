from stocks import Stocks
import AutomateEmail
import StockData
from apscheduler.schedulers.background import BackgroundScheduler
import Db as Db
def main():
    print("Starting...")
    my_db = Db('stock.db')
    stock_system = Stocks(my_db)
    email = AutomateEmail.AutomateEmail()
    sched = BackgroundScheduler()

    for stock in stock_system.myDatabase:
        stock_system.update_add_stock(stock)
        # none then email.renotify() does not need to run
    stock_system.end_of_day()
    stock_system.end_of_week()
    def automate():
        stock_system.update_prices(email)  # calls automate email

    def end_of_day():
        stock_system.end_of_day()

    def end_of_week():
        stock_system.end_of_week()

    #sched.add_job(automate, 'cron', day_of_week='*', hour='*', minute='*', second='1,20,40,59', timezone='US/Eastern') #test
    sched.add_job(automate, 'cron', day_of_week='mon-fri', hour='9-16', minute='*', second='1,31', timezone='US/Eastern')
    sched.add_job(end_of_day, 'cron', day_of_week='mon-fri', hour='16', minute='0', second=0, timezone='US/Eastern')
    sched.add_job(end_of_week, 'cron', day_of_week='fri', hour='16', minute='0', second=0, timezone='US/Eastern')

    sched.start()

main()
