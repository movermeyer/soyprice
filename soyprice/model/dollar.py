from core import Variable


class BlueDollar(Variable):

    def __init__(self, cache):
        super(BlueDollar, self).__init__(cache)
        self.name = 'dollar/blue'

    def scrap(self, date_list):
        # Return a list of prices
        url = ("http://www.ambito.com/economia/mercados/monedas/dolar/"
               "x_dolar_get_grafico.asp?ric=ARSB=&tipo=yyyy")
        dollars = map(
            lambda (d, v): (datetime.datetime.strptime(d, "%Y/%m/%d").date(), v),
            eval(requests.get(url).text))
        dollars = filter(lambda (d, v): d in date_list, dollars)
        return map(lambda (d, v): v, dollars)
