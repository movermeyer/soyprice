import unittest
from soyprice import statistic
from soyprice.model import database as db
from soyprice.model.dollar import BlueDollar
import datetime


class TestRegression(unittest.TestCase):

    def setUp(self):
        self.day = datetime.date(2014, 10, 8)
        self.date_list = map(lambda i: self.day - datetime.timedelta(days=i),
                             range(1,8))
        self.cache = db.open()
        self.dollar = BlueDollar(self.cache)
        self.regression = statistic.Regression(self.date_list,
                                               self.day,
                                               [self.dollar])

    def test_future_x(self):
        self.assertEquals(self.regression.future_x, 735514)

    def test_get_data(self):
        x, y = self.regression.get_data(self.regression.variables[0])
        self.assertEquals(x, [735513, 735512, 735509, 735508, 735507])
        self.assertEquals(y, [14.7, 14.95, 15.3, 15.5, 15.6])

    def test_degree(self):
        self.assertEquals(self.regression.degree, 2)

    def test_weights(self):
        x, y = self.regression.get_data(self.regression.variables[0])
        self.assertEquals(self.regression.weights(x), [1, 1, 1, 1, 1])
        self.assertEquals(self.regression.weights(x[0:2]), [1, 1])

    def test_pattern(self):
        fx, estimated, rmse = self.regression.pattern()
        self.assertAlmostEqual(fx(735514), 14.553, 3)
        self.assertAlmostEqual(fx(735515), 14.366, 3)
        tests = zip(estimated,
                    [14.7308, 14.899, 15.346, 15.4765, 15.597])
        map(lambda (res, ref): self.assertAlmostEqual(res, ref, 3), tests)
        self.assertAlmostEqual(rmse, 0.0353, 3)

    def test_check(self):
        # It don't check nothing.
        pass

    def test_resume(self):
        x, y, estimated, weights, rmse, next_x, next_y = self.regression.resume()
        self.assertEquals(x, [735513, 735512, 735509, 735508, 735507])
        self.assertEquals(y, [14.7, 14.95, 15.3, 15.5, 15.6])
        tests = zip(estimated, [14.7308, 14.899, 15.346, 15.4765, 15.597])
        map(lambda (res, ref): self.assertAlmostEqual(res, ref, 3), tests)
        self.assertAlmostEqual(rmse, 0.0353, 3)
        self.assertEquals(next_x, self.regression.future_x)
        self.assertAlmostEqual(next_y, 14.553, 3)


if __name__ == '__main__':
    unittest.main()
