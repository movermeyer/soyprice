#!/usr/bin/env python
# -*- coding: utf-8 -*-

from twython import Twython, TwythonError
import datetime
from scraper import get_dataset, get_days, get_next_workable_day, date_to_int
from statistic import forecast
import pylab as pl
from PIL import Image
from StringIO import StringIO
import numpy as np



APP_KEY = 'rogbcg4oUIEHGh35kxMVGAf2k'
APP_SECRET = 'skkBp744JPEAXDnz0O3ZgxPX4qOpGU4Ao7rW588w1FTx4Laax4'
OAUTH_TOKEN = '282317077-WksqawGHtDE7ROc02ptId5Uei22hWEpnUe8NmGY9'
OAUTH_TOKEN_SECRET = 'ZaXiSkd4KIEiL7gf8OK63i4BteILTQKDaCNNOC5jhYHtm'
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)


def tweet(status, image):
    photo = open(image, 'rb')
    template = "%s [https://github.com/limiear/soyprice]"
    twitter.update_status_with_media(media=photo, status=template % status)


def graph(x, y, fix, next_x, next_y):
    border = 2
    ratio = 100
    x_values = list(x) + [next_x]
    limits_x = min(x_values), max(x_values)
    y_values = list(y) + [next_y]
    limits_y = min(y_values), max(y_values)
    pl.figure(figsize=(8, 4), dpi=100)
    pl.subplot(1, 1, 1)
    pl.plot(x, y, color="blue", linewidth=0.0, linestyle="-", marker=".")
    pl.plot(x, fix, color="red", linewidth=1.0, linestyle="-",)
    pl.plot([next_x], [next_y], color="red", marker="o")
    pl.xlim(*limits_x)
    pl.xticks(np.linspace(limits_x[0] - border, limits_x[1] + border, (limits_x[1] - limits_x[0] + border * 2 + 1) / 10, endpoint=True))
    pl.ylim(*limits_y)
    pl.yticks(np.linspace(limits_y[0] - border * ratio, limits_y[1] + border * ratio, 5, endpoint=True))
    pl.xlabel('date', fontsize=10)
    pl.ylabel('AR$', fontsize=10)
    filename = "graph.png" 
    pl.savefig(filename, dpi=100)
    return filename


def step():
    try:
        amount = 100
        date_list = get_days(datetime.datetime.today(), range(0, amount))
	date_list.reverse()
        x, y = get_dataset(date_list, places=['san'])
        day = get_next_workable_day(date_list[-1])
	next_x = date_to_int(day)
        price, fix, fx = forecast(x, y, next_x)
	filename = graph(x, y, fix, next_x, fx(next_x))
        tweet('Forecast Soja San Martín con descarga para el %s: AR$%.f' %
              (day.strftime('%d-%m-%Y'), price), filename)
    except TwythonError as e:
        pass

step()
