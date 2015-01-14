import unittest
from soyprice import statistic
from soyprice.model import database as db
from soyprice.model.dollar import BlueDollar
import datetime


class TestTimeRegression(unittest.TestCase):

    def setUp(self):
        self.day = datetime.date(2014, 10, 8)
        self.date_list = map(lambda i: self.day - datetime.timedelta(days=i),
                             range(1,8))
        self.cache = db.open()
        self.dollar = BlueDollar(self.cache)
        self.regression = statistic.TimeRegression(self.date_list,
                                                   self.day,
                                                   [self.dollar])

    def test_description(self):
        self.assertEquals(self.regression.description,
                          self.regression.variables[0].description)

    def test_reference(self):
        self.assertEquals(self.regression.reference,
                          self.regression.variables[0].reference)

    def test_degree(self):
        self.assertEquals(self.regression.degree, 3)

    def test_weights(self):
        x, y = self.regression.get_data(self.regression.variables[0])
        tests = zip(self.regression.weights(x),
                    [-0.0, 0.1666, 0.6666, 0.8333, 1.0])
        map(lambda (res, ref): self.assertAlmostEqual(res, ref, 3), tests)
        self.assertEquals(self.regression.weights(x[0:1]), [1])

    def test_check(self):
        # With only one variable don't raise nothing.
        self.regression.check()
        # With more than 1 variable it should raise an exception.
        self.regression.variables.append(self.dollar)
        with self.assertRaisesRegexp(Exception,
                                     'TimeRegression should have only '
                                     '1 variable.'):
            self.regression.check()
        # Without variables it should raise an exception.
        self.regression.variables = []
        with self.assertRaisesRegexp(Exception,
                                     'TimeRegression should have only '
                                     '1 variable.'):
            self.regression.check()


if __name__ == '__main__':
    unittest.main()
