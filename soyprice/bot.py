#!/usr/bin/env python
# -*- coding: utf-8 -*-

from twython import Twython, TwythonError
import requests
from bs4 import BeautifulSoup as beautifulsoup
import datetime
import re
from numpy import polyfit, poly1d
from itertools import chain


APP_KEY = 'rogbcg4oUIEHGh35kxMVGAf2k'
APP_SECRET = 'skkBp744JPEAXDnz0O3ZgxPX4qOpGU4Ao7rW588w1FTx4Laax4'
OAUTH_TOKEN = '282317077-WksqawGHtDE7ROc02ptId5Uei22hWEpnUe8NmGY9'
OAUTH_TOKEN_SECRET = 'ZaXiSkd4KIEiL7gf8OK63i4BteILTQKDaCNNOC5jhYHtm'


# Requires Authentication as of Twitter API v1.1
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

def get_price(row):
    fix_string = lambda x: x.lower().strip(' \.\-')
    text = lambda x: fix_string(x.encode('utf-8').decode('ascii', 'ignore'))
    fix_float = lambda x: re.sub('\,', '.', re.sub('\.\.', '.', x))
    cast = lambda x: float(fix_float(x)) if len(x) > 0 and x[0].isdigit() else text(x)
    numdays = 10
    texts = lambda row, tag: [cast(c.text) for c in row.select(tag)]
    return texts(row, 'th') + texts(row,'td')


def get_prices(datetime):
    date = datetime.strftime('%d-%m-%Y')
    url = ('http://diario.afascl.coop/afaw/afa-tablas/dispo.do?tk=1414884447433&'
           'mode=get&fecha=%s&_=' % date)
    page = beautifulsoup(requests.get(url).text)
    rows = page.select('tr')
    prices = [get_price(r) for r in rows]
    soy_present = lambda x: 'soja' in x[0] and 'san' in x[1] and 'con descarga' in x[4] and x[2] > 0
    present = lambda x: {'datetime': datetime.date(), 'price': x[2], 'port':x[1]}
    prices = map(present, filter(soy_present, prices))
    return datetime.date(), prices

try:
    numdays = 17
    base = datetime.datetime.today()
    date_list = [base - datetime.timedelta(days=x) for x in range(0, numdays)]
    prices = map(lambda (dt, x): (dt, [p['price'] for p in x]), map(get_prices, date_list))
    prices = filter(lambda x: len(x[1]) > 0, prices)
    params = map(lambda x: x[1], prices)
    idx = range(len(params),0,-1)
    x = [[idx[i]] * len(params[i]) for i in range(len(params))]
    x = list(chain(*x))
    y = list(chain(*params))
    fit = polyfit(x, y, 3)
    fx = poly1d(fit)
    forecast = fx(x[0] + 1)
    twitter.update_status(status='Forecast Soja con descarga: $%.f' % forecast)
except TwythonError as e:
    print e
