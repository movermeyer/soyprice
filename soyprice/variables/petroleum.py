from variables.core import app, db, get_var, request, Change
from datetime import datetime, timedelta


#@app.run_every("day", "12:30")
dt = datetime.now() + timedelta(minutes=1)
@app.run_every("day", dt.strftime("%H:%M"))
def update_petroleum_wti_barrel_ratios():
    url = ("http://www.ambito.com/economia/mercados/petroleo/"
           "x_petroleo_get_grafico.asp?ric=1&"
           "timeFrom={:}&timeTo={:}&tipo=libre")
    begin = datetime(1984, 4, 12)
    end = datetime.now()
    petroleum_vars = {
        "PETROLEUM": {
            "name": "petroleum/wti",
            "description": "Petroleo West Texas Intermediate",
            "reference": "USD/barrel"
        }
    }
    for k, v in petroleum_vars.items():
        variable = get_var(**v)
        begin = (variable.changes.order_by("moment desc").first().moment
                 if variable.changes.count() else begin)
        p = lambda dt: dt.strftime("%d/%m/%Y")
        composed_url = url.format(p(begin), p(end))
        prices = map(
            lambda (d, v): (datetime.strptime(d, "%Y/%m/%d").date(), v),
            eval(request(composed_url)))
        for d, v in prices:
            ch = Change(value=v, moment=d)
            variable.changes.append(ch)
            db.session.add(ch)
        db.session.add(variable)
        db.session.commit()
