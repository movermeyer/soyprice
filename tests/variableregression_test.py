import unittest
from soyprice import statistic
from soyprice.model import database as db
from soyprice.model.dollar import BlueDollar
from soyprice.model.soy import SanMartin
import datetime


class TestVariableRegression(unittest.TestCase):

    def setUp(self):
        self.day = datetime.date(2014, 10, 8)
        self.date_list = map(lambda i: self.day - datetime.timedelta(days=i),
                             range(1, 8))
        self.cache = db.open()
        self.dollar = BlueDollar(self.cache)
        self.sanmartin = SanMartin(self.cache)
        self.regression = statistic.VariableRegression(self.date_list,
                                                       self.day,
                                                       [self.dollar,
                                                        self.sanmartin])

    def test_description(self):
        names = map(lambda v: v.description, self.regression.variables)
        description = '%s vs. %s' % tuple(names)
        self.assertEquals(self.regression.description, description)

    def test_reference(self):
        self.assertEquals(self.regression.reference, '')

    def test_degree(self):
        self.assertEquals(self.regression.degree, 1)

    def test_weights(self):
        x, y, dt = self.regression.get_data(self.regression.variables[0])
        self.assertEquals(self.regression.weights(x),
                          [1.0, 1.0, 1.0, 1.0, 1.0])
        self.assertEquals(self.regression.weights(x[0:1]), [1])

    def test_check(self):
        # With only one variable don't raise nothing.
        self.regression.check()
        # With more than 2 variable it should raise an exception.
        self.regression.variables.append(self.dollar)
        with self.assertRaisesRegexp(Exception,
                                     'VariableRegression should have always '
                                     '2 variables.'):
            self.regression.check()
        # Without variables it should raise an exception.
        self.regression.variables = [self.dollar]
        with self.assertRaisesRegexp(Exception,
                                     'VariableRegression should have always '
                                     '2 variables.'):
            self.regression.check()

    def test_data(self):
        x, y, dt = self.regression.data
        self.assertEquals(x, [14.95, 15.6, 15.5, 15.3])
        self.assertEquals(y, [2270.0, 2260.0, 2250.0, 2220.0])
        self.assertEquals(dt, [735512, 735507, 735508, 735509])

    def test_future_x(self):
        self.assertEquals(self.regression.future_x, 15.3)


if __name__ == '__main__':
    unittest.main()
