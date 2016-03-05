#! /usr/bin/python

import model.database as db
import simplejson as json
from datetime import datetime, date


def encode_datetime(o):
    if isinstance(o, date) or isinstance(o, datetime):
        return o.isoformat()
    return o


def cleaning(o):
    return {encode_datetime(k): cleaning(v)
            for k, v in o.items()} if isinstance(o, dict) else o


def translate():
    data = db.open()
    for k in data.keys():
        with open("{:}.json".format(k), "w") as f:
            json.dump(cleaning(db.get(data, k)), f)
    db.close(data)
