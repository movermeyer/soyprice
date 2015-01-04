import unittest
from soyprice.model import database as db
from soyprice.model.soy import SanMartin
import os
import datetime
import requests


class TestSanMartin(unittest.TestCase):

    def setUp(self):
        os.remove('cache.db')
        self.cache = db.open()
        self.var = SanMartin(self.cache)
        self.date_list = [datetime.date(2014,9,8) + datetime.timedelta(days=i)
                          for i in range(3)]
        self.today_list = [datetime.datetime.now().date()]
        self.values = [2330., 2320., 2310.]

    def tearDown(self):
        db.close(self.cache)

    def test_scrap(self):
        result = self.var.scrap(self.date_list)
        self.assertEquals(result, self.values)


if __name__ == '__main__':
    unittest.main()
