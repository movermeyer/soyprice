import unittest
import abstract
from soyprice.model import database as db
from soyprice.model.soy import SanMartin
import datetime


class TestSanMartin(abstract.TestCase):

    def setUp(self):
        self.remove('cache*')
        self.cache = db.open()
        self.var = SanMartin(self.cache)
        self.date_list = [datetime.date(2014, 9, 8) +
                          datetime.timedelta(days=i)
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
