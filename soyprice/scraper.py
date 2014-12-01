import datetime
import requests
from bs4 import BeautifulSoup as beautifulsoup
from itertools import chain
import re
import json
import database as db


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


class Variable(object):

    def __init__(self, cache):
        self.cache = cache
        self.name = 'global'

    @property
    def today(self):
        return datetime.datetime.now().date()

    def scrap(self, date_list):
        pass

    def should_scrap(self, date):
        serie = db.get(self.cache, self.name)
        return (date not in serie.keys()
                or (date == self.today and serie[date] is None))

    def get_element(self, date):
        # Return a price
        if isinstance(date, datetime.datetime):
            date = date.date()
        if self.should_scrap(date):
            price = self.scrap([date])
            price = price[0] if len(price) else price
            db.get(self.cache, self.name)[date] = price
            db.sync(self.cache)
        data = db.get(self.cache, self.name)
        return data[date] if date in data.keys() else None

    def get(self, date_list=[]):
        # Return a list of tuples with date and price for each tuple
        return map(lambda d: (d, self.get_element(d)), date_list)


class BlueDollar(Variable):

    def __init__(self, cache):
        super(BlueDollar, self).__init__(cache)
        self.name = 'dollar/blue'

    def scrap(self, date_list):
        # Return a list of prices
        url = ("http://www.ambito.com/economia/mercados/monedas/dolar/"
               "x_dolar_get_grafico.asp?ric=ARSB=&tipo=yyyy")
        dollars = map(
            lambda (d, v): (datetime.datetime.strptime(d, "%Y/%m/%d").date(), v),
            eval(requests.get(url).text))
        dollars = filter(lambda (d, v): d in date_list, dollars)
        return map(lambda (d, v): v, dollars)


class Soy(Variable):

    def __init__(self, cache):
        super(Soy, self).__init__(cache)
        self.name = 'soy'


class Chicago(Soy):

    def __init__(self, cache):
        super(Chicago, self).__init__(cache)
        self.name += '/chicago'

    def scrap(self, date_list):
        if date_list[0] != self.today:
            return [None]
        url = 'http://www.indexmundi.com/commodities/?commodity=soybeans'
        page = beautifulsoup(requests.get(url).text)
        prices = map(lambda x: float(x.text),
                     page.select('#divDaily .dailyPrice'))
        return prices


class Afascl(Soy):

    def __init__(self, cache):
        super(Afascl, self).__init__(cache)
        self.name += '/afascl'

    def scrap_date(self, date, place):
        print date, place
        date_str = date.strftime('%d-%m-%Y')
        url = ('http://diario.afascl.coop/afaw/afa-tablas/dispo.do?'
               'tk=1414884447433&mode=get&fecha=%s&_=' % date_str)
        page = beautifulsoup(requests.get(url).text)
        rows = page.select('tr')
        fix_string = lambda x: x.lower().strip(' \.\-')
        text = lambda x: fix_string(x.encode('utf-8').decode('ascii', 'ignore'))
        fix_float = lambda x: re.sub('\,', '.', re.sub('\.\.', '.', x))
        cast = (lambda x: float(fix_float(x))
                if len(x) > 0 and x[0].isdigit() else text(x))
        texts = lambda row, tag: [cast(c.text) for c in row.select(tag)]
        get_price = lambda row: texts(row, 'th') + texts(row,'td')
        prices = map(get_price, rows)
        soy_with_download = lambda x: ('soja' in x[0] and 'con descarga' in x[4]
                                  and x[2] > 0 and place in x[1])
        prices = map(lambda x: x[2],
                        filter(soy_with_download, prices))
        return prices


class SanMartin(Afascl):

    def __init__(self, cache):
        super(SanMartin, self).__init__(cache)
        self.name += '/sanmartin'

    def scrap(self, date_list):
        prices = map(lambda d: self.scrap_date(d, 'san'),
                     date_list)
        return list(chain(*prices))


def get_dollars(cache, date_list=[]):
    v = BlueDollar(cache)
    return v.get(date_list)


def get_chicago_price(cache, date_list=[]):
    v = Chicago(cache)
    return v.get(date_list)


def get_prices(cache, date_list):
    v = SanMartin(cache)
    return v.get(date_list)


def get_dataset(cache, date_list=[], places=[]):
    adapt = lambda p: (date_to_int(p['datetime']), p['price'])
    prices = {}
    prices['chicago'] = get_chicago_price(cache, date_list)
    prices['afascl'] = get_prices(cache, date_list, places)
    params = list(chain(*prices['afascl']))
    print params
    x, y = zip(*params)
    return x, y
