from stocks import Stocks
import AutomateEmail

from apscheduler.schedulers.background import BackgroundScheduler
from Db import Db


def main():
    print("Starting...")
    db = Db('stock.db')
    stock_system = Stocks()
    email = AutomateEmail.AutomateEmail()
    sched = BackgroundScheduler()
    # cleaned list
    # !!! every single query I make will need to be fixed...
    my_list = db.stock_list()
    for stock in my_list:
        print("processing %s" % stock)
        stock_system.update_add_stock(stock, db)
    # stock_system.update_prices(email, db)
    # none then email.renotify() does not need to run

    # stock_system.end_of_week()
    def automate():
        stock_system.update_prices(email)  # calls automate email

    def end_of_day():
        stock_system.end_of_day()

    def end_of_week():
        stock_system.end_of_week()

    # sched.add_job(automate, 'cron', day_of_week='*', hour='*', minute='*', second='1,20,40,59', timezone='US/Eastern') #test
    sched.add_job(automate, 'cron', day_of_week='mon-fri', hour='9-16', minute='*', second='1,31',
                  timezone='US/Eastern')
    sched.add_job(end_of_day, 'cron', day_of_week='mon-fri', hour='16', minute='0', second=0, timezone='US/Eastern')
    # sched.add_job(end_of_week, 'cron', day_of_week='fri', hour='16', minute='0', second=0, timezone='US/Eastern')

    sched.start()


main()
