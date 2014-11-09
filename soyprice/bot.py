#!/usr/bin/env python
# -*- coding: utf-8 -*-

from twython import Twython, TwythonError
import datetime
from scraper import get_dataset, get_days, get_next_workable_day, date_to_int, get_dollars
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


def graph(x, y, fix, next_x, next_y, dollars, fix_d, next_d_x, next_d_y ):
    border = 2
    ratio = 100
    x_values = list(x) + [next_x]
    y_values = list(y) + [next_y]
    limits = (min(x_values) - border,
              max(x_values) + border,
              min(y_values) - border * ratio,
              max(y_values) + border * ratio)
    pl.figure(figsize=(8, 4), dpi=100)
    pl.title('Soja puerto San Martin por @limiear')
    ax = pl.subplot(1, 1, 1)
    ax.axis(limits)
    ax.scatter(x, y, marker=".", linewidth=0.5)
    ax.plot(x, fix, color="red", linewidth=1.0, linestyle="-",)
    ax.plot([next_x], [next_y], color="red", marker="o")
    pl.xticks([], 0, endpoint=True)
    pl.xlabel("ventana de %i dias previos" % (x[-1] + 1 - x[0]), fontsize=10)
    pl.ylabel('AR$', fontsize=10)
    ax.yaxis.tick_right()
    ax.yaxis.set_label_position("right")
    # bx = pl.subplot(2, 1, 2)
    # bx.scatter(*zip(*dollars))
    # pl.plot(x, fix_d, color="red", linewidth=1.0, linestyle="-",)
    # pl.plot([next_d_x], [next_d_y], color="red", marker="o")
    # bx.yaxis.tick_right()
    # bx.yaxis.set_label_position("right")
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
        price, rmse, fix, fx = forecast(x, y, next_x)
        dollars = get_dollars(date_list)
        price_d, rmse_d, fix_d, fx_d = forecast(*(zip(*dollars) + [next_x]))
	filename = graph(x, y, fix, next_x, fx(next_x), dollars, fix_d, next_x, price_d)
        tweet(('Forecast Soja puerto San Martín con descarga para el'
               ' %s: AR$ %.f (RMSE: AR$ %i)') % 
                (day.strftime('%d-%m-%Y'), price, int(rmse)),
               filename)
    except TwythonError as e:
        pass

step()
