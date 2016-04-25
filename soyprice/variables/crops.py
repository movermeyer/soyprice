# -*- coding: utf-8 -*-
from variables.core import (app, variable, get_page, requests,
                            beautifulsoup, get_next_date, change,
                            update_prices, GET)
from datetime import datetime, date, timedelta
from functools import partial
from glob import glob
import re
import json


def load_bcr_dataset(filename, variables):
    with open(filename, "r") as f:
        data = beautifulsoup(f.read(), "xml")
        details = data.findAll("Detail")
        for d in details:
            product = d.attrs['Producto']
            moment = datetime.strptime(d.attrs['fchOper'], "%d/%m/%Y").date()
            try:
                price = float(d.attrs['PrcFij'][2:])
                change(value=price,
                       moment=moment.strftime('%Y-%m-%d'),
                       variable_id=variables[product]['id'])
            except ValueError, e:
                print e


is_float = lambda v: re.match("^\d+?\.\d+?$", v)


#dt = datetime.now() + timedelta(minutes=1)
#@app.run_every("day", dt.strftime("%H:%M"))
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
    variables = {k: variable(**v) for k, v in bcr_variables.items()}
    is_empty = len(variables["Soja"]['changes']) == 0
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
        begin = get_next_date(var)
        prices = map(lambda v: float(v) if is_float(v) else None, line[2:])
        prices = zip(dts, prices)
        update_prices(var, prices, begin)


def get_afascl_prices(dt, variables):
    if dt.weekday() > 4:
        # 0: mon ... 4:fri 5:sat 6: sun
        print "Detected {:} as a weekend day.".format(str(dt))
        return {}
    if dt.date() >= date(2014, 12, 1):
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
            results.append((detect[0][1]['id'], reg[2]))
    return dict(results)


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
    variables = {k: variable(**v) for k, v in afascl_variables.items()}
    get_prices = partial(get_afascl_prices, variables=variables)
    dt = get_next_date(variables['Soja'], date(2007, 10, 1))
    while dt.date() <= date.today():
        for variable_id, price in get_prices(dt).items():
            change(value=price,
                   moment=dt.strftime('%Y-%m-%d'),
                   variable_id=variable_id)
        dt += timedelta(days=1)


@app.run_every("day", "17:00")
def update_crops_chicago():
    chicago_variables = {
        u"soybean": {
            "name": u"soy/chicago",
            "description": u"Soja de la Bolsa de Chicago (USA)",
            "reference": u"USD/bushel"
        }
    }
    variables = {k: variable(**v) for k, v in chicago_variables.items()}
    url = "http://api.ieconomics.com/ie5/?s=s%201:com&span=1y&_="
    data = get_page(url).select('p')[0].text
    data = json.loads(data)[0]
    data = data['series'][0]['serie']['data']
    to_tuple = (lambda r:
                (datetime.strptime(r['x_dt'], "%Y-%m-%dT%H:%M:%S.%fZ").date(),
                 float(r['close'])))
    prices = map(to_tuple, data)
    for k, var in variables.items():
        begin = get_next_date(var)
        update_prices(var, prices, begin)
