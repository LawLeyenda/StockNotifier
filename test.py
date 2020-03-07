import apscheduler
from apscheduler.schedulers.blocking import BlockingScheduler


def job_function():
    print("Hello World")

def job_function1():
    print("Hello Worldedfefr")



sched = BlockingScheduler()

# Schedules job_function to be run on the third Friday
# of June, July, August, November and December at 00:00, 01:00, 02:00 and 03:00
# sched.add_job(job_function, 'cron', month='*', day='*', hour='*', minute='*', second=20)

sched.add_job(job_function, 'cron', day_of_week='mon-fri', second='1,16,31,46,59', timezone='US/Eastern')
sched.add_job(job_function1, 'cron', day_of_week='mon-fri', hour='4', minute=0, second=0, timezone='US/Eastern')

sched.start()

# Runs from Monday to Friday at 5:30 (am) until 2014-05-30 00:00:00
