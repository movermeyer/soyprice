import datetime
import requests
from bs4 import BeautifulSoup as beautifulsoup
from itertools import chain
import re


def get_days(base, defined_range=range(0,15)):
    return [base - datetime.timedelta(days=x) for x in defined_range]


def get_next_workable_day(date):
    calculate = lambda d: d + datetime.timedelta(days=1)
    day = calculate(date)
    while day.weekday() > 4:
        day = calculate(day)
    return day


def get_price(row):
    fix_string = lambda x: x.lower().strip(' \.\-')
    text = lambda x: fix_string(x.encode('utf-8').decode('ascii', 'ignore'))
    fix_float = lambda x: re.sub('\,', '.', re.sub('\.\.', '.', x))
    cast = lambda x: float(fix_float(x)) if len(x) > 0 and x[0].isdigit() else text(x)
    numdays = 20
    texts = lambda row, tag: [cast(c.text) for c in row.select(tag)]
    return texts(row, 'th') + texts(row,'td')


def get_prices(datetime, places=[]):
    date = datetime.strftime('%d-%m-%Y')
    url = ('http://diario.afascl.coop/afaw/afa-tablas/dispo.do?tk=1414884447433&'
           'mode=get&fecha=%s&_=' % date)
    page = beautifulsoup(requests.get(url).text)
    rows = page.select('tr')
    prices = [get_price(r) for r in rows]
    soy_with_download = lambda x: ('soja' in x[0] and 'con descarga' in x[4]
                                   and x[2] > 0)
    present = lambda x: {'datetime': datetime.date(), 'price': x[2], 'port':x[1]}
    prices = map(present, filter(soy_with_download, prices))
    if places:
        soy_in_places = lambda p: any([place in p['port'] for place in places])
        prices = filter(soy_in_places, prices)
    return datetime.date(), prices

def get_dataset(date_list=[], places=[]):
    adapt = lambda p: (int(p['datetime'].toordinal()), p['price'])
    prices = map(lambda (dt, prices): map(adapt, prices),
                 map(get_prices, date_list))
    prices = filter(lambda day: len(day) > 0, prices)
    params = list(chain(*prices))
    x, y = zip(*params)
    return x, y
