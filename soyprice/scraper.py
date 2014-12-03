import datetime
from model.soy import SanMartin, Chicago
from model.dollar import BlueDollar


def get_days(base, defined_range=range(0,15)):
    return [base.date() - datetime.timedelta(days=x) for x in defined_range]


def get_next_workable_day(date):
    calculate = lambda d: d + datetime.timedelta(days=1)
    day = calculate(date)
    while day.weekday() > 4:
        day = calculate(day)
    return day


def date_to_int(dt):
    return int(dt.toordinal())


def get_dollars(cache, date_list=[]):
    v = BlueDollar(cache)
    return v
    # return v.get(date_list)

def get_chicago_price(cache, date_list=[]):
    v = Chicago(cache)
    return v
    # return v.get(date_list)


def get_prices(cache, date_list):
    v = SanMartin(cache)
    return v
    # return v.get(date_list)
