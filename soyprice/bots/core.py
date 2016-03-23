from database import db
from models import Variable as Var
from datetime import datetime


class Variable(object):

    def __init__(self, name):
        self.name = name
        self.variable = db.session.query(Var).filter_by(name=name).first()
        self.description = self.variable.description
        self.reference = self.variable.reference

    @property
    def today(self):
        return datetime.now().date()

    def get(self, date_list=[]):
        dates = date_list.copy()
        dates = map(lambda d: d.date() if isinstance(d, datetime) else d,
                    dates)
        elements = filter(lambda ch: ch.moment in dates,
                          self.variable.changes.all())
        return map(lambda e: (e.moment, e.value), elements)
