import unittest
from soyprice import scraper
import datetime


class TestScraper(unittest.TestCase):

    def setUp(self):
        self.day = datetime.datetime(2014,10,8)
        self.prices = (
            datetime.date(2014, 10, 8),
            [
                {'price': 2260.0,
                 'port': u'san martn',
                 'datetime': datetime.date(2014, 10, 8)},
                {'price': 2140.0,
                 'port': u'b.blanca',
                 'datetime': datetime.date(2014, 10, 8)},
                {'price': 2090.0,
                 'port': u'quequen',
                 'datetime': datetime.date(2014, 10, 8)},
                {'price': 2210.0,
                 'port': u'ramallo',
                 'datetime': datetime.date(2014, 10, 8)},
                {'price': 2080.0,
                 'port': u'daireaux',
                 'datetime': datetime.date(2014, 10, 8)}
            ])

    def test_get_prices(self):
        prices = scraper.get_prices(self.day)
        self.assertEquals(prices, self.prices)


    def test_get_prices_san_martin_and_blanca(self):
        prices = scraper.get_prices(self.day, places=['san', 'blan'])
        only_san_and_blanca = lambda x: x['port'] in ['san martn', 'b.blanca']
        prices_tmp = list(self.prices)
        prices_tmp[1] = filter(only_san_and_blanca, prices_tmp[1])
        self.assertEquals(prices, tuple(prices_tmp))


if __name__ == '__main__':
    unittest.main()
