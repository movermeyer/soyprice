import datetime
import requests
from bs4 import BeautifulSoup as beautifulsoup
from itertools import chain
import re
import json
import database as db


def get_days(base, defined_range=range(0,15)):
    return [base - datetime.timedelta(days=x) for x in defined_range]


def get_next_workable_day(date):
    calculate = lambda d: d + datetime.timedelta(days=1)
    day = calculate(date)
    while day.weekday() > 4:
        day = calculate(day)
    return day


def get_chicago_price(cache, datetime):
    path = 'soy/chicago'
    date = datetime.date()
    today = datetime.now().date()
    prices = 0
    if date not in db.get(cache, path).keys() and date == today:
        url = 'http://www.indexmundi.com/commodities/?commodity=soybeans'
        page = beautifulsoup(requests.get(url).text)
        prices = page.select('#divDaily .dailyPrice')[0].text
        db.get(cache, path)[datetime.date()] = prices
        db.sync(cache)
    elif date == today:
        prices = db.get(cache, path)[datetime.date()]
    return date, prices


def get_prices(cache, datetime, places=[]):
    path = 'soy/afascl'
    date = datetime.date()
    if date not in db.get(cache, path).keys():
        date_str = datetime.strftime('%d-%m-%Y')
        url = ('http://diario.afascl.coop/afaw/afa-tablas/dispo.do?'
               'tk=1414884447433&mode=get&fecha=%s&_=' % date_str)
        page = beautifulsoup(requests.get(url).text)
        rows = page.select('tr')
        fix_string = lambda x: x.lower().strip(' \.\-')
        text = lambda x: fix_string(x.encode('utf-8').decode('ascii', 'ignore'))
        fix_float = lambda x: re.sub('\,', '.', re.sub('\.\.', '.', x))
        cast = lambda x: float(fix_float(x)) if len(x) > 0 and x[0].isdigit() else text(x)
        texts = lambda row, tag: [cast(c.text) for c in row.select(tag)]
        get_price = lambda row: texts(row, 'th') + texts(row,'td')
        prices = map(get_price, rows)
        soy_with_download = lambda x: ('soja' in x[0] and 'con descarga' in x[4]
                                   and x[2] > 0)
        present = lambda x: {'datetime': date,
                             'price': x[2], 'port':x[1]}
        prices = map(present, filter(soy_with_download, prices))
        db.get(cache, path)[date] = prices
        db.sync(cache)
    else:
        prices = db.get(cache, path)[date]
    if places:
        soy_in_places = lambda p: any([place in p['port'] for place in places])
        prices = filter(soy_in_places, prices)
    return date, prices


def date_to_int(dt):
    return int(dt.toordinal())


def get_dataset(cached, date_list=[], places=[]):
    adapt = lambda p: (date_to_int(p['datetime']), p['price'])
    prices = {}
    prices['chicago'] = map(lambda (dt, prices): (date_to_int(dt), prices),
                           [get_chicago_price(cached, d)
                            for d in date_list])
    prices['afascl'] = map(lambda (dt, prices): map(adapt, prices),
                           [get_prices(cached, d, places) for d in date_list])
    prices['afascl'] = filter(lambda day: len(day) > 0, prices['afascl'])
    params = list(chain(*prices['afascl']))
    x, y = zip(*params)
    return x, y


def get_dollars(date_list=[]):
    date_tmp = map(lambda d: d.date(), date_list)
    url = ("http://www.ambito.com/economia/mercados/monedas/dolar/"
           "x_dolar_get_grafico.asp?ric=ARSB=&tipo=yyyy")
    dollars = eval(requests.get(url).text)
    dollars = map(lambda (d, v): (datetime.datetime.strptime(d, "%Y/%m/%d"), v),
                  dollars)
    dollars = filter(lambda (d, v): d.date() in date_tmp, dollars)
    return map(lambda (d, v): [date_to_int(d), v], dollars)
