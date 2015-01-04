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

    def test_forecast(self):
        result = statistic.forecast(self.dollar, self.date_list, self.day)
        price, rmse, estimated, fx, weights = result
        self.assertAlmostEqual(price, 14.60, 2)
        self.assertAlmostEqual(rmse, 0.019, 2)
        refs = [14.753, 14.900, 15.330, 15.470, 15.608]
        map(lambda test: self.assertAlmostEqual(test[0], test[1], 2),
            zip(estimated, refs))
        self.assertNotIn(fx.__class__, [float, int, list])
        refs = [-0.0, 0.166, 0.666, 0.83, 1.0]
        map(lambda test: self.assertAlmostEqual(test[0], test[1], 2),
            zip(weights, refs))

if __name__ == '__main__':
    unittest.main()
