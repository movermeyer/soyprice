import datetime


def get_days(base, defined_range=range(0,15)):
    return [base.date() - datetime.timedelta(days=x) for x in defined_range]


def get_next_workable_day(date):
    calculate = lambda d: d + datetime.timedelta(days=1)
    day = calculate(date)
    while day.weekday() > 4:
        day = calculate(day)
    return day
