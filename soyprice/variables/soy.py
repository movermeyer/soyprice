# -*- coding: utf-8 -*-
from variables.core import app, db, get_var, request, beautifulsoup, Change
from datetime import datetime
from functools import partial
from glob import glob
from decimal import Decimal, InvalidOperation
import re


def load_dataset(filename, variables):
    with open(filename, "r") as f:
        data = beautifulsoup(f.read(), "xml")
        details = data.findAll("Detail")
        for d in details:
            product = d.attrs['Producto']
            moment = datetime.strptime(d.attrs['fchOper'], "%d/%m/%Y").date()
            try:
                price = Decimal(d.attrs['PrcFij'][2:])
                ch = Change(value=price, moment=moment)
                variables[product].changes.append(ch)
                db.session.add(ch)
            except InvalidOperation:
                pass
        list(map(db.session.add, variables.values()))
        db.session.commit()


@app.run_every("day", "10:55")
def update_soy_bcr():
    bcr_prices = {
        u"Soja": {
            "name": u"soy/bcr",
            "description": u"Soja de la Bolsa de Comercio de Rosario (Arg)",
            "reference": u"ARS/tn"
        },
        u"Trigo": {
            "name": u"wheat/bcr",
            "description": u"Trigo de la Bolsa de Comercio de Rosario (Arg)",
            "reference": u"ARS/tn"
        },
        u"Sorgo": {
            "name": u"sorghum/bcr",
            "description": u"Sorgo de la Bolsa de Comercio de Rosario (Arg)",
            "reference": u"ARS/tn"
        },
        u'Ma\xedz': {
            "name": u"corn/bcr",
            "description": u"Maiz de la Bolsa de Comercio de Rosario (Arg)",
            "reference": u"ARS/tn"
        },
        u"Girasol": {
            "name": u"sunseed/bcr",
            "description": u"Girasol de la Bolsa de Comercio de Rosario (Arg)",
            "reference": u"ARS/tn"
        }
    }
    variables = {k: get_var(**v) for k, v in bcr_prices.items()}
    is_empty = variables["Soja"].changes.count() == 0
    if is_empty:
        datasets = glob('data/bcr/*.prices.xml')
        load_data = partial(load_dataset, variables=variables)
        map(load_data, datasets)
    url = 'http://www.bcr.com.ar/Pages/Granos/Cotizaciones/default.aspx'
    page = beautifulsoup(request(url))
    rows = page.select('.ms-vb tr')
    text = map(lambda r: [c.text for c in r.select('td')], rows)
    to_date = lambda d: datetime.strptime(d, '%d/%m/%Y').date()
    dts = map(to_date, text[0][2:])
    for line in text[2:]:
        var = variables[line[0]]
        last_reg = var.changes.order_by("moment desc").first()
        is_float = lambda v: re.match("^\d+?\.\d+?$", v)
        prices = map(lambda v: float(v) if is_float(v) else None, line[2:])
        prices = zip(dts, prices)
        for moment, price in filter(lambda r: r[1] and r[1] > last_reg,
                                    prices):
            ch = Change(value=price, moment=moment)
            db.session.add(ch)
            var.changes.append(ch)
        db.session.add(var)


update_soy_bcr()
