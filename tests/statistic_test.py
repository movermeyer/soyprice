import unittest
from soyprice import statistic
import datetime


class TestStatistic(unittest.TestCase):

    def setUp(self):
        self.day = datetime.date(2014, 10, 8)

    def test_date_to_int(self):
        number = statistic.date_to_int(self.day)
        self.assertEquals(number, 735514)
        number = statistic.date_to_int(self.day + datetime.timedelta(days=3))
        self.assertEquals(number, 735514 + 3)


if __name__ == '__main__':
    unittest.main()
