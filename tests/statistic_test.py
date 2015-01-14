import unittest
from soyprice import statistic
from soyprice.model import database as db
from soyprice.model.dollar import BlueDollar
import datetime


class TestStatistic(unittest.TestCase):

    def setUp(self):
        self.day = datetime.date(2014, 10, 8)
        self.date_list = map(lambda i: self.day - datetime.timedelta(days=i),
                             range(1,8))
        self.cache = db.open()
        self.dollar = BlueDollar(self.cache)

    def tearDown(self):
        db.close(self.cache)

    def test_date_to_int(self):
        number = statistic.date_to_int(self.day)
        self.assertEquals(number, 735514)
        number = statistic.date_to_int(self.day + datetime.timedelta(days=3))
        self.assertEquals(number, 735514 + 3)


if __name__ == '__main__':
    unittest.main()
