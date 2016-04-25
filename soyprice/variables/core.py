from application import app
from config import config
import requests
from bs4 import BeautifulSoup as beautifulsoup
import json
from datetime import datetime, timedelta


def GET(url):
    return requests.get(url).text


def POST(url, data):
    headers = {'content-type': 'application/json'}
    return requests.post(url, data=json.dumps(data), headers=headers).text


def get_var(**kwargs):
    variable_name = kwargs["name"]
    url = ('{:}api/variable?q='
           '{{"filters":[{{"name":"name","op":"eq","val":"{:}"}}],'
           '"single":"true"}}').format(config['URL'], variable_name)
    result = GET(url)
    return json.loads(result)


def set_var(**kwargs):
    url = '{:}api/variable'.format(config['URL'])
    result = POST(url, data=kwargs)
    return json.loads(result)


def variable(**kwargs):
    instance = get_var(**kwargs)
    if instance.keys() == ["message"]:
        instance = set_var(**kwargs)
    return instance


def change(**kwargs):
    url = '{:}api/change'.format(config['URL'])
    result = POST(url, data=kwargs)
    return json.loads(result)


def get_page(url):
    return beautifulsoup(GET(url))


def get_next_date(var, default=datetime(1984, 4, 12)):
    changes = sorted(var['changes'], key=lambda c: c['moment'],
                     reverse=True)
    begin = (datetime.strptime(changes[0]['moment'], "%Y-%m-%d")
             if changes else default)
    begin += timedelta(days=1)
    return begin


def update_prices(var, prices, begin):
    prices = filter(lambda d: d[0] >= begin.date(), prices)
    for d, v in prices:
        if v:
            change(value=v,
                   moment=d.strftime('%Y-%m-%d'),
                   variable_id=var['id'])
