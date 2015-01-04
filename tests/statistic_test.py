import unittest
from soyprice import statistic
import datetime


class TestStatistic(unittest.TestCase):

    def setUp(self):
        self.day = datetime.date(2014, 10, 8)
        pass

    def test_(self):
        pass

    def test_date_to_int(self):
        number = statistic.date_to_int(self.day)
        self.assertEquals(number, 735514)

if __name__ == '__main__':
    unittest.main()
