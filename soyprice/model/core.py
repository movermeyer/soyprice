import database as db
import datetime
import requests


class Variable(object):

    def __init__(self, cache):
        self.cache = cache
        self.name = 'global'
        self.description = ''
        self.reference = ''

    @property
    def today(self):
        return datetime.datetime.now().date()

    def request(self, url):
        return requests.get(url).text

    def scrap(self, date_list):
        pass

    def should_scrap(self, date):
        serie = db.get(self.cache, self.name)
        return (date not in serie.keys()
                or (date == self.today and serie[date] is None))

    def get_element(self, date):
        # Return a price
        if isinstance(date, datetime.datetime):
            date = date.date()
        if self.should_scrap(date):
            price = self.scrap([date])
            price = price[0] if len(price) else price
            db.get(self.cache, self.name)[date] = price
            db.sync(self.cache)
        data = db.get(self.cache, self.name)
        return data[date] if date in data.keys() else None

    def get(self, date_list=[]):
        # Return a list of tuples with date and price for each tuple
        return map(lambda d: (d, self.get_element(d)), date_list)
