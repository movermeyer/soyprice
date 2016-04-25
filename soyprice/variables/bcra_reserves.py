# -*- coding: utf-8 -*-
from variables.core import (app, beautifulsoup, variable, update_prices,
                            get_next_date, POST)
from datetime import datetime, timedelta


dt = datetime.now() + timedelta(minutes=1)
@app.run_every("day", dt.strftime("%H:%M"))
#@app.run_every("day", "20:30")
def update_bcra_reserves():
    url = "http://www.bcra.gov.ar/Estadisticas/estprv010001.asp"
    bcra_vars = {
        u"reserve": {
            u"name": u"reserve/bcra",
            u"description": u"Reservas en dolares del Banco Central de la República Argentina",
            u"reference": u"USD"
        }
    }
    variables = {k: variable(**v) for k, v in bcra_vars.items()}
    var = variables["reserve"]
    first_date = datetime(1996, 03, 02)
    data = {
        'desde': first_date.strftime("%d/%m/%Y"),
        'hasta': datetime.now().strftime("%d/%m/%Y"),
        'descri': 1,
        'I1.x': 40,
        'I1.y': 7,
        'I1': 'Enviar',
        'fecha': 'Fecha_Serie',
        'campo': 'Res_Int_BCRA'
    }
    page = beautifulsoup(POST(url, data))
    rows = page.select("#texto_columna_2 tr")
    data = map(lambda r: map(lambda c: c.text, r.select('td')), rows)
    data = data[1:]
    reserves = map(lambda d:
                   (datetime.strptime(d[0], "%d/%m/%Y").date(),
                    float(d[1]) * 1000000),
                   data)
    print reserves
    begin = get_next_date(var, first_date)
    print begin
    update_prices(var, reserves, begin)
    print "ready!"
