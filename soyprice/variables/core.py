from application import app
from database import db
from models import Variable, Change
import requests
from bs4 import BeautifulSoup as beautifulsoup


def get_var(**kwargs):
    instance = db.session.query(Variable).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = Variable(**kwargs)
        db.session.add(instance)
        db.session.commit()
    return instance


def request(url):
    return requests.get(url).text


def get_page(url):
    return beautifulsoup(request(url))
