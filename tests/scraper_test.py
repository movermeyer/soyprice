import unittest
from soyprice import scraper
from soyprice.model import database
import datetime


class TestScraper(unittest.TestCase):

    def setUp(self):
        self.day = datetime.date(2014,10,8)
        self.prices = [(datetime.date(2014, 10, 8), 2260.0)]
        self.days = [datetime.date(2014, 10, 8) - datetime.timedelta(days=x)
                     for x in range(0, 15)]
        self.cache = database.open()

    def tearDown(self):
        database.close(self.cache)

    def test_get_days(self):
        days = scraper.get_days(datetime.datetime(2014, 10, 8))
        self.assertEquals(days, self.days)

    def test_get_next_workable_day(self):
        day = scraper.get_next_workable_day(self.day)
        self.assertEquals(day, datetime.date(2014, 10, 9))
        day = scraper.get_next_workable_day(datetime.date(2014, 10, 10))
        self.assertEquals(day, datetime.date(2014, 10, 13))


if __name__ == '__main__':
    unittest.main()
