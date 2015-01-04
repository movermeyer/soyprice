import unittest
import abstract
from soyprice.model import database as db
from soyprice.model.soy import Chicago
import os
import datetime
import requests


class TestChicago(abstract.TestCase):

    def setUp(self):
        self.remove('cache*')
        self.cache = db.open()
        self.var = Chicago(self.cache)
        self.date_list = [datetime.date(2014,10,8) + datetime.timedelta(days=i)
                          for i in range(3)]
        self.values = [None, None, None]

    def tearDown(self):
        db.close(self.cache)

    def test_scrap(self):
        self.assertEquals(self.var.scrap(self.date_list),
                          list(set(self.values)))

    def test_get(self):
        # It query by an old date_list and it obtains all None (because
        # the cache is empty).
        values = self.var.get(self.date_list)
        self.assertEquals(values, zip(self.date_list, self.values))
        # It ask by the today value, and it return a real value.
        date_list = [datetime.datetime.now()]
        values = self.var.get(date_list)
        self.assertGreater(values[0][1], 0.)



if __name__ == '__main__':
    unittest.main()
