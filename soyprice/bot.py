#!/usr/bin/env python
# -*- coding: utf-8 -*-

from twython import Twython, TwythonError
import datetime
from scraper import get_dataset, get_days, get_next_workable_day
from statistic import forecast


APP_KEY = 'rogbcg4oUIEHGh35kxMVGAf2k'
APP_SECRET = 'skkBp744JPEAXDnz0O3ZgxPX4qOpGU4Ao7rW588w1FTx4Laax4'
OAUTH_TOKEN = '282317077-WksqawGHtDE7ROc02ptId5Uei22hWEpnUe8NmGY9'
OAUTH_TOKEN_SECRET = 'ZaXiSkd4KIEiL7gf8OK63i4BteILTQKDaCNNOC5jhYHtm'
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)


def tweet(status):
    # Requires Authentication as of Twitter API v1.1
    template = "%s [https://github.com/limiear/soyprice]"
    twitter.update_status(status=template % status)


def step():
    try:
        numdays = 17
        date_list = get_days(datetime.datetime.today())
        x, y = get_dataset(date_list)
        price = forecast(x, y)
        day = (get_next_workable_day(date_list[0])).strftime('%d-%m-%Y')
        tweet('Forecast Soja con descarga para el %s: AR$%.f' %
              (day, price))
    except TwythonError as e:
        pass

step()
