import models
from datetime import datetime


class Variable(object):

    def __init__(self, name):
        self.name = name
        self.variable = models.Variable.query.filter_by(name=name).first()
        self.description = self.variable.description
        if not self.description:
            self.description = ''
        self.reference = self.variable.reference

    @property
    def today(self):
        return datetime.now().date()

    def get(self, date_list=[]):
        changes = self.variable.changes.order_by("moment").all()
        elements = filter(lambda ch: ch.moment in date_list, changes)
        return map(lambda e: (e.moment, float(e.value)), elements)
