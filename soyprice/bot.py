#!/usr/bin/env python
# -*- coding: utf-8 -*-

from twython import Twython, TwythonError
import datetime
from numpy import polyfit, poly1d
from itertools import chain
from scraper import get_prices


APP_KEY = 'rogbcg4oUIEHGh35kxMVGAf2k'
APP_SECRET = 'skkBp744JPEAXDnz0O3ZgxPX4qOpGU4Ao7rW588w1FTx4Laax4'
OAUTH_TOKEN = '282317077-WksqawGHtDE7ROc02ptId5Uei22hWEpnUe8NmGY9'
OAUTH_TOKEN_SECRET = 'ZaXiSkd4KIEiL7gf8OK63i4BteILTQKDaCNNOC5jhYHtm'
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)


def tweet(status):
    # Requires Authentication as of Twitter API v1.1
    twitter.update_status(status=status)


def obtain(date_list):
    prices = map(lambda (dt, x): (dt, [p['price'] for p in x]),
                 map(get_prices, date_list))
    prices = filter(lambda x: len(x[1]) > 0, prices)
    params = map(lambda x: x[1], prices)
    idx = range(len(params),0,-1)
    x = [[idx[i]] * len(params[i]) for i in range(len(params))]
    x = list(chain(*x))
    y = list(chain(*params))
    return x, y


def forecast(date_list):
    x, y = obtain(date_list)
    fit = polyfit(x, y, 3)
    fx = poly1d(fit)
    return fx(x[0] + 1)


def get_next_workable_day(date):
    calculate = lambda d: d + datetime.timedelta(days=1)
    day = calculate(date)
    while day.weekday() > 4:
        day = calculate(date)
    return day


try:
    numdays = 17
    base = datetime.datetime.today()
    date_list = [base - datetime.timedelta(days=x) for x in range(0, numdays)]
    price = forecast(date_list)
    day = (get_next_workable_day(date_list[0])).strftime('%d-%m-%Y')
    tweet('Forecast Soja con descarga para el %s: $%.f' %
          (day, price))
except TwythonError as e:
    print e
