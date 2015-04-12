from core import Variable
from bs4 import BeautifulSoup as beautifulsoup
from itertools import chain
import re
import datetime
from goslate import Goslate


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


class BCR(Soy):
    def __init__(self, cache):
        super(BCR, self).__init__(cache)
        self.name += '/bcr'
        self.description = 'Soja en Rosario'
        self.reference = 'AR$/TN'

    def scrap(self, date_list):
        url = 'http://www.bcr.com.ar/Pages/Granos/Cotizaciones/default.aspx'
        page = beautifulsoup(self.request(url))
        rows = page.select('.ms-vb tr')
        text = map(lambda r: [c.text for c in r.select('td')], rows)
        to_date = lambda d: datetime.datetime.strptime(d, '%d/%m/%Y').date()
        dts = map(to_date, filter(lambda r: 'Fixing date' in r, text)[0][2:])
        is_float = lambda v: re.match("^\d+?\.\d+?$", v)
        prices = map(lambda v: float(v) if is_float(v) else None,
                     filter(lambda r: 'soybean' in r, text)[0][2:])
        prices = dict(filter(lambda p: p[1], zip(dts, prices)))
        prices = map(lambda dt: prices[dt],
                     filter(lambda dt: dt in prices, date_list))
        return prices


class Afascl(Soy):

    def __init__(self, cache):
        super(Afascl, self).__init__(cache)
        self.name += '/afascl'
        self.translator = Goslate()

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

    def obtain_page(self, date):
        get_page = lambda url: beautifulsoup(self.request(url))
        url = 'http://afascl.coop/afadiario/home/diario.php'
        page = get_page(url)
        diary = page.select('.preciosdiario span')[0].text.split('\r\n')[0]
        diary = self.translator.translate(diary.lower(), "en", "es")
        diary = datetime.datetime.strptime(diary, '%A %B %d, %Y').date()
        if (diary != date):
            date_str = date.strftime('%d-%m-%Y')
            url = ('http://diario.afascl.coop/afaw/afa-tablas/dispo.do?'
                   'tk=1414884447433&mode=get&fecha=%s&_=' % date_str)
            page = get_page(url)
        return page

    def scrap_date(self, date, place):
        page = self.obtain_page(date)
        return self.obtain_prices(page, place)


class SanMartin(Afascl):

    def __init__(self, cache):
        super(SanMartin, self).__init__(cache)
        self.name += '/sanmartin'
        self.description = 'Soja puerto San Martin'

    def scrap(self, date_list):
        prices = map(lambda d: self.scrap_date(d, 'san'),
                     date_list)
        return list(chain(*prices))
