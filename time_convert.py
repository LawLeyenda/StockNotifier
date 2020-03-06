import pytz
import datetime

#broken method
def convert(the_datetime):
    utc_now = pytz.utc.localize(the_datetime)
    eastern = utc_now.astimezone(pytz.timezone("US/Eastern"))
    return eastern
