from datetime import datetime
from variables.core import get_var


class Variable(object):

    def __init__(self, name):
        self.name = name
        self.variable = get_var(name)
        self.description = self.variable['description']
        self.reference = self.variable['reference']

    @property
    def today(self):
        return datetime.now().date()

    def to_date(self, moment):
        return datetime.strptime(moment, "%Y-%m-%d").date()

    def get(self, date_list=[]):
        changes = sorted(self.variable['changes'], key=lambda c: c["moment"])
        elements = filter(lambda ch: ch['moment'] in date_list, changes)
        return map(lambda e: (self.to_date(e['moment']), float(e['value'])),
                   elements)
