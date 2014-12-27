from core import Variable
from bs4 import BeautifulSoup as beautifulsoup
from itertools import chain
import re
import datetime
from translate import Translator


class Soy(Variable):

    def __init__(self, cache):
        super(Soy, self).__init__(cache)
        self.name = 'soy'
        self.reference = 'ARS/TN'


class Chicago(Soy):

    def __init__(self, cache):
        super(Chicago, self).__init__(cache)
        self.name += '/chicago'
        self.description = 'Soja en Chicago'
        self.reference = 'USD/TN'

    def scrap(self, date_list):
        if date_list[0] != self.today:
            return [None]
        url = 'http://www.indexmundi.com/commodities/?commodity=soybeans'
        page = beautifulsoup(self.request(url))
        prices = map(lambda x: float(x.text),
                     page.select('#divDaily .dailyPrice'))
        return prices


class Afascl(Soy):

    def __init__(self, cache):
        super(Afascl, self).__init__(cache)
        self.name += '/afascl'
        self.translator = Translator(from_lang="es", to_lang="en")

    def obtain_prices(self, page, place):
        rows = page.select('tr')
        fix_string = lambda x: x.lower().strip(' \.\-')
        text = (lambda x: fix_string(x.encode('utf-8')
                                     .decode('ascii', 'ignore')))
        fix_float = lambda x: re.sub('\d*\,\d*', '.',
                                     re.sub('\d*\.\.\d*', '.', x))
        is_digit = lambda x: x.isdigit()
        all_digits = lambda x: all(map(is_digit, x))
        cast = lambda x: float(x) if all_digits(x.split('.')) else text(x)
        texts = lambda row, tag: [cast(fix_float(c.text))
                                  for c in row.select(tag)]
        get_price = lambda row: texts(row, 'th') + texts(row, 'td')
        prices = map(get_price, rows)
        soy_with_download = lambda x: ('soja' in x[0]
                                       and 'con descarga' in x[4]
                                       and x[2] > 0 and place in x[1])
        return map(lambda x: x[2],
                   filter(soy_with_download, prices))

    def scrap_date(self, date, place):
        if date == self.today:
            url = 'http://afascl.coop/afadiario/home/diario.php'
        else:
            date_str = date.strftime('%d-%m-%Y')
            url = ('http://diario.afascl.coop/afaw/afa-tablas/dispo.do?'
                   'tk=1414884447433&mode=get&fecha=%s&_=' % date_str)
        page = beautifulsoup(self.request(url))
        has_price = True
        if date == self.today:
            today = page.select('.preciosdiario span')[0].text.split('\r\n')[0]
            today = self.translator.translate(today.lower())
            today = datetime.datetime.strptime(today, '%A %B %d, %Y').date()
            has_price = (today == self.today)
        return self.obtain_prices(page, place) if has_price else []


class SanMartin(Afascl):

    def __init__(self, cache):
        super(SanMartin, self).__init__(cache)
        self.name += '/sanmartin'
        self.description = 'Soja puerto San Martin'

    def scrap(self, date_list):
        prices = map(lambda d: self.scrap_date(d, 'san'),
                     date_list)
        return list(chain(*prices))
