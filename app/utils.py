from datetime import datetime
import pytz

def get_now_central():
    """Returns the current datetime in US/Central timezone."""
    central = pytz.timezone('US/Central')
    return datetime.now(central)

def get_today_central():
    """Returns the current date in US/Central timezone."""
    return get_now_central().date()
