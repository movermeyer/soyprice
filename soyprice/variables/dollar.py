from variables.core import app, db, get_var, request, Change
from datetime import datetime


@app.run_every("day", "10:30")
def update_dollars_ratios():
    url = ("http://www.ambito.com/economia/mercados/monedas/dolar/"
           "x_dolar_get_grafico.asp?ric={:}&tipo={:}")
    dollar_vars = {
        "ARSB=": {
            "name": "dollar/blue",
            "description": "Dolar blue en Argentina",
            "reference": "ARS/USD"
        },
        "ARSSCBCRA": {
            "name": "dollar/bcra",
            "description": "Dolar del Banco Central de la Republica Argentina",
            "reference": "ARS/USD"
        }
    }
    for k, v in dollar_vars.items():
        variable = get_var(**v)
        lapse = "ww" if variable.changes.count() else "yyyy"
        composed_url = url.format(k, lapse)
        dollars = map(
            lambda (d, v): (datetime.strptime(d, "%Y/%m/%d").date(), v),
            eval(request(composed_url)))
        dts = map(lambda ch: ch.moment, variable.changes.all())
        if dts:
            dollars = filter(lambda (d, v): d[0] not in dts, dollars)
        for d, v in dollars:
            ch = Change(value=v, moment=d)
            variable.changes.append(ch)
            db.session.add(ch)
        db.session.add(variable)
        db.session.commit()
