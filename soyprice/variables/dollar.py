from variables.core import app, variable, get_next_date, update_prices, GET
from datetime import datetime, timedelta


#dt = datetime.now() + timedelta(minutes=1)
#@app.run_every("day", dt.strftime("%H:%M"))
@app.run_every("day", "10:30")
def update_dollars_ratios():
    url = ("http://www.ambito.com/economia/mercados/monedas/dolar/"
           "x_dolar_get_grafico.asp?ric={:}&tipo={:}")
    begin = datetime(1984, 4, 12)
    dollar_vars = {
        "ARSB=": {
            "name": u"dollar/blue",
            "description": u"Dolar blue en Argentina",
            "reference": u"ARS/USD"
        },
        "ARSSCBCRA": {
            "name": u"dollar/bcra",
            "description": (u"Dolar del Banco Central de la Republica "
                            "Argentina"),
            "reference": u"ARS/USD"
        }
    }
    for k, v in dollar_vars.items():
        var = variable(**v)
        lapse = "ww" if var['changes'] else "yyyy"
        composed_url = url.format(k, lapse)
        dollars = map(
            lambda (d, v): (datetime.strptime(d, "%Y/%m/%d").date(), v),
            eval(GET(composed_url)))
        begin = get_next_date(var)
        update_prices(var, dollars, begin)
