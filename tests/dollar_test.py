import unittest
import abstract
from soyprice.model import database as db
from soyprice.model.dollar import BlueDollar
import os
import datetime
import requests


class TestDollar(abstract.TestCase):

    def setUp(self):
        self.remove('cache*')
        self.cache = db.open()
        self.var = BlueDollar(self.cache)
        self.date_list = [datetime.date(2014,10,8) + datetime.timedelta(days=i)
                          for i in range(3)]
        self.values = [14.65, 14.83, 14.95]

    def tearDown(self):
        db.close(self.cache)

    def test_scrap(self):
        self.assertEquals(self.var.scrap(self.date_list), self.values)

    def test_get(self):
        # It query by a date_list.
        values = self.var.get(self.date_list)
        self.assertEquals(values, zip(self.date_list, self.values))


if __name__ == '__main__':
    unittest.main()
