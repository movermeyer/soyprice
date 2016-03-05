from database import db


class Change(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    moment = db.Column(db.Date, nullable=False, index=True)
    value = db.Column(db.Numeric(10, 5), nullable=False)
    variable_id = db.Column(db.Integer, db.ForeignKey('variable.id'))


class Variable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, unique=True)
    description = db.Column(db.Unicode)
    reference = db.Column(db.Unicode)
    changes = db.relationship("Change", backref="variable", lazy="dynamic")

    def __repr__(self):
        return self.name


db.create_all()
