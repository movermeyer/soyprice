from variables.core import app, variable, update_prices, get_next_date, GET
from datetime import datetime, timedelta


#dt = datetime.now() + timedelta(minutes=1)
#@app.run_every("day", dt.strftime("%H:%M"))
@app.run_every("day", "12:30")
def update_petroleum_wti_barrel_ratios():
    url = ("http://www.ambito.com/economia/mercados/petroleo/"
           "x_petroleo_get_grafico.asp?ric=1&"
           "timeFrom={:}&timeTo={:}&tipo=libre")
    begin = datetime(1984, 4, 12)
    end = datetime.now()
    petroleum_vars = {
        u"PETROLEUM": {
            u"name": u"petroleum/wti",
            u"description": u"Petroleo West Texas Intermediate",
            u"reference": u"USD/barrel"
        }
    }
    for k, v in petroleum_vars.items():
        var = variable(**v)
        begin = get_next_date(var, begin)
        p = lambda dt: dt.strftime("%d/%m/%Y")
        composed_url = url.format(p(begin), p(end))
        prices = map(
            lambda (d, v): (datetime.strptime(d, "%Y/%m/%d").date(), v),
            eval(GET(composed_url)))
        prices = filter(lambda p: p[0] >= begin.date(), prices)
        update_prices(var, prices, begin)
