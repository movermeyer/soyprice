# -*- coding: utf-8 -*-
from variables.core import app, db, get_var, get_page, beautifulsoup, Change
from datetime import datetime, date, timedelta
from functools import partial
from glob import glob
from decimal import Decimal, InvalidOperation
import re
import requests


def load_bcr_dataset(filename, variables):
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
            except InvalidOperation, e:
                print e
        list(map(db.session.add, variables.values()))
        db.session.commit()


is_float = lambda v: re.match("^\d+?\.\d+?$", v)


@app.run_every("day", "10:55")
def update_crops_bcr():
    bcr_variables = {
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
    variables = {k: get_var(**v) for k, v in bcr_variables.items()}
    is_empty = variables["Soja"].changes.count() == 0
    if is_empty:
        datasets = glob('data/bcr/*.prices.xml')
        load_data = partial(load_bcr_dataset, variables=variables)
        map(load_data, datasets)
    url = 'http://www.bcr.com.ar/Pages/Granos/Cotizaciones/default.aspx'
    rows = get_page(url).select('.ms-vb tr')
    text = map(lambda r: [c.text for c in r.select('td')], rows)
    to_date = lambda d: datetime.strptime(d, '%d/%m/%Y').date()
    dts = map(to_date, text[0][2:])
    for line in text[2:]:
        var = variables[line[0]]
        last_reg = var.changes.order_by("moment desc").first()
        prices = map(lambda v: float(v) if is_float(v) else None, line[2:])
        prices = zip(dts, prices)
        for moment, price in filter(lambda r: r[1] and r[1] > last_reg,
                                    prices):
            ch = Change(value=price, moment=moment)
            db.session.add(ch)
            var.changes.append(ch)
        db.session.add(var)


def get_afascl_prices(dt, variables):
    if dt.weekday() > 4:
        # 0: mon ... 4:fri 5:sat 6: sun
        print "Detected {:} as a weekend day.".format(str(dt))
        return {}
    if dt >= date(2014, 12, 1):
        url = "http://afascl.coop/afadiario/home/diario_xml.php"
        dt_str = dt.strftime("%d/%m/%Y")
        page = beautifulsoup(requests.post(url, data={"fecha": dt_str}).text)
        table = page.select(".tblprecios")
    else:
        dt_str = dt.strftime("%d-%m-%Y")
        url = ("http://diario.afascl.coop/afaw/afa-tablas/dispo.do?"
               "mode=get&fecha={:}&_=").format(dt_str)
        page = beautifulsoup(requests.get(url).text)
        table = page.select(".table_home")
    if not table:
        return {}
    table = table[0]
    rows = table.select('tr')
    text = map(lambda r: [c.text for c in r.select("th") + r.select("td")],
               rows)
    important_text = map(lambda r: r[:3] + [r[4]], text)
    prices = filter(lambda r: u"San Mart" in r[1], important_text)
    lower_variables = map(lambda r: (r[0].lower(), r[1]), variables.items())
    results = []
    for reg in prices:
        detect = filter(lambda lv: lv[0] in reg[0].lower(), lower_variables)
        if detect and is_float(reg[2]):
            results.append((detect[0][1], reg[2]))
    return dict(results)


#dt = datetime.now() + timedelta(minutes=1)
#@app.run_every("day", dt.strftime("%H:%M"))
@app.run_every("day", "11:50")
def update_crops_afascl():
    afascl_variables = {
        u"Soja": {
            "name": u"soy/afascl",
            "description": u"Soja de la AFSCL de San Martin (Arg)",
            "reference": u"ARS/tn"
        },
        u"Trigo": {
            "name": u"wheat/afascl",
            "description": u"Trigo de la AFSCL de San Martin (Arg)",
            "reference": u"ARS/tn"
        },
        u"Sorgo": {
            "name": u"sorghum/afscl",
            "description": u"Sorgo de la AFSCL de San Martin (Arg)",
            "reference": u"ARS/tn"
        },
        u'Ma\xedz': {
            "name": u"corn/afascl",
            "description": u"Maiz de la AFSCL de San Martin (Arg)",
            "reference": u"ARS/tn"
        },
        u"Girasol": {
            "name": u"sunseed/afascl",
            "description": u"Girasol de la AFSCL de San Martin (Arg)",
            "reference": u"ARS/tn"
        }
    }
    variables = {k: get_var(**v) for k, v in afascl_variables.items()}
    begin = date(2007, 10, 1)
    last_reg = variables['Soja'].changes.order_by("moment desc").first()
    dt = last_reg.moment if last_reg else begin
    get_prices = partial(get_afascl_prices, variables=variables)
    while dt <= date.today():
        for variable, price in get_prices(dt).items():
            ch = Change(value=price, moment=dt)
            db.session.add(ch)
            variable.changes.append(ch)
        db.session.commit()
        dt += timedelta(days=1)
    list(map(db.session.add, variables.values()))
    db.session.commit()
