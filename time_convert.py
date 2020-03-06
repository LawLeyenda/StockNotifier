import pytz
import datetime


# broken method
def localize(the_datetime):
    utc_now = pytz.utc.localize(the_datetime)
    eastern = utc_now.astimezone(pytz.timezone("US/Eastern"))
    return eastern
