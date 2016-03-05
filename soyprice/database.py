from application import app
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates


db = SQLAlchemy(app)
