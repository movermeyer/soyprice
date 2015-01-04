import unittest
import abstract
from soyprice.model import database as db
from soyprice.model.soy import Afascl
import datetime
import requests


class TestAfascl(abstract.TestCase):

    def setUp(self):
        self.remove('cache*')
        self.cache = db.open()
        self.var = Afascl(self.cache)
        self.date_list = [datetime.date(2014,10,8) + datetime.timedelta(days=i)
                          for i in range(3)]
        self.today = datetime.datetime.now().date()
        self.values = {
            'bla': [2140., 2140., 2120.],
            'san': [2260., 2300., 2300.]
        }

    def tearDown(self):
        db.close(self.cache)

    def test_scrap_date(self):
        for place, values in self.values.items():
            result = map(lambda x: self.var.scrap_date(x, place)[0],
                         self.date_list)
            self.assertEquals(result, values)

    def test_scrap_today_date(self):
        result = self.var.scrap_date(self.today, 'san')
        self.assertGreater(result, 0.)


if __name__ == '__main__':
    unittest.main()
