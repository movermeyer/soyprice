#!/usr/bin/env python
# -*- coding: utf-8 -*-

from twython import Twython, TwythonError
import datetime
from scraper import get_prices, get_chicago_price, get_days, get_next_workable_day, date_to_int, get_dollars
from statistic import forecast
import numpy as np
import database as db
from grapher import graph


APP_KEY = 'rogbcg4oUIEHGh35kxMVGAf2k'
APP_SECRET = 'skkBp744JPEAXDnz0O3ZgxPX4qOpGU4Ao7rW588w1FTx4Laax4'
OAUTH_TOKEN = '282317077-WksqawGHtDE7ROc02ptId5Uei22hWEpnUe8NmGY9'
OAUTH_TOKEN_SECRET = 'ZaXiSkd4KIEiL7gf8OK63i4BteILTQKDaCNNOC5jhYHtm'
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)


def tweet(status, image):
    photo = open(image, 'rb')
    template = "%s [https://github.com/limiear/soyprice]"
    twitter.update_status_with_media(media=photo, status=template % status)




def step():
    cache = db.open()
    try:
        amount = 30
        date_list = get_days(datetime.datetime.today(), range(0, amount))
	date_list.reverse()
        day = get_next_workable_day(date_list[-1])
	next_x = date_to_int(day)
        # dollars
        dollars = get_dollars(cache, date_list)
        params = zip(*dollars) + [next_x]
        price_d, rmse_d, fix_d, fx_d, weights = forecast(*params)
        # soy
        afascl = get_prices(cache, date_list)
        chicago = get_chicago_price(cache, date_list)
        params = zip(*afascl) + [next_x]
        price, rmse, fix, fx, weights = forecast(*params)
        print price_d
        params = zip(*afascl) + [fix , next_x , fx(next_x), dollars,
                                 fix_d, next_x, price_d, rmse, weights]
        filename = graph(*params)
        tweet(('Forecast Soja puerto San Martín con descarga para el'
               ' %s: AR$ %.f (RMSE: AR$ %i)') %
                (day.strftime('%d-%m-%Y'), price, int(rmse)),
               filename)
    except TwythonError as e:
        pass
    db.close(cache)

step()
