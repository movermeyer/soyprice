from application import app
from database import db
from flask.ext.restless import APIManager
from models import Change, Variable


manager = APIManager(app, flask_sqlalchemy_db=db)
manager.create_api(Change, methods=['GET'])
manager.create_api(Variable, methods=['GET'])
