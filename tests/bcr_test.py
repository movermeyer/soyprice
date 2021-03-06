import unittest
import abstract
from soyprice.model import database as db
from soyprice.model.soy import BCR
import datetime


class TestBCR(abstract.TestCase):

    def setUp(self):
        self.remove('cache*')
        self.cache = db.open()
        self.var = BCR(self.cache)
        self.date_list = [datetime.date(2014, 10, 8) +
                          datetime.timedelta(days=i)
                          for i in range(3)]
        self.today = datetime.datetime.now().date()
        self.yesterday = self.today - datetime.timedelta(days=1)
        self.values = {
            'rosario': [2260., 2300., 2300.]
        }

    def tearDown(self):
        db.close(self.cache)

    def test_scrap(self):
        self.assertEquals(self.var.scrap(self.date_list), [])
        prices = self.var.scrap([self.today])
        price = prices[0] if prices else self.var.scrap([self.yesterday])
        self.assertGreater(price, 1000.)


if __name__ == '__main__':
    unittest.main()
