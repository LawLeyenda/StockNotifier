from stocks import Stocks
import AutomateEmail
from news import stock_news
from apscheduler.schedulers.background import BackgroundScheduler
from Db import Db


def main():
    print("Starting...")
    db = Db('stock.db')
    stock_system = Stocks()
    news = stock_news()
    email = AutomateEmail.AutomateEmail()
    sched = BackgroundScheduler()
    # cleaned list
    # my_list = db.stock_list()
    # for stock in my_list:
    #     print("processing %s" % stock)
    #     stock_system.update_add_stock(stock, db)
    #     news.query_news(stock, db)
    #
    # stock_system.end_of_day(db)

    # stock_system.end_of_week()


    def automate():
        print("Updating prices and sending email")
        stock_system.update_prices(email, news, db)  # calls automate email

    def end_of_day():
        stock_system.end_of_day(db)
        for stock in my_list:
            news.query_news(stock, db)

    def end_of_week():
        stock_system.end_of_week(db, email)
    #
    sched.add_job(automate, 'cron', day_of_week='mon-fri', hour='9-16', minute='*', second='1,31', timezone='US/Eastern') #test
    # sched.add_job(automate, 'cron', hour='*', minute='*', second='1,31',
    #               timezone='US/Eastern')
    sched.add_job(end_of_day, 'cron', day_of_week='mon-fri', hour='16', minute='0', second=0, timezone='US/Eastern')
    sched.add_job(end_of_week, 'cron', day_of_week='fri', hour='16', minute='0', second=0, timezone='US/Eastern')
    #
    sched.start()


main()
