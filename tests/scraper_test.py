import unittest
from soyprice import database, scraper
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
        self.days = [datetime.datetime(2014, 10, 8) - datetime.timedelta(days=x)
                     for x in range(0, 15)]
        self.cache = database.open()

    def tearDown(self):
        database.close(self.cache)

    def test_get_days(self):
        days = scraper.get_days(datetime.datetime(2014, 10, 8))
        self.assertEquals(days, self.days)

    def test_get_next_workable_day(self):
        day = scraper.get_next_workable_day(self.day)
        self.assertEquals(day, datetime.datetime(2014, 10, 9))
        day = scraper.get_next_workable_day(datetime.datetime(2014, 10, 10))
        self.assertEquals(day, datetime.datetime(2014, 10, 13))

    def test_get_prices(self):
        prices = scraper.get_prices(self.cache, self.day)
        self.assertEquals(prices, self.prices)

    def test_get_prices_san_martin_and_blanca(self):
        prices = scraper.get_prices(self.cache, self.day, places=['san', 'blan'])
        only_san_and_blanca = lambda x: x['port'] in ['san martn', 'b.blanca']
        prices_tmp = list(self.prices)
        prices_tmp[1] = filter(only_san_and_blanca, prices_tmp[1])
        self.assertEquals(prices, tuple(prices_tmp))

    def test_get_dataset(self):
        # prices = scraper.get_dataset(self.day)
        pass  # print prices


if __name__ == '__main__':
    unittest.main()
