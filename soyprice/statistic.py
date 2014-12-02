from numpy import polyfit, poly1d, sqrt
from math import log, e

def date_to_int(dt):
    return int(dt.toordinal())

def forecast(variable, day):
    data = filter(lambda d: d[1], variable)
    if len(data) == 0:
        return 0., 0., 0., lambda x: x, (1.)
    x, y = zip(*data)
    x = map(date_to_int, x)
    weights = map(lambda xi: (xi -x[0])/float(x[-1] - x[0]), x)
    fit = polyfit(x, y, 6, w=weights)
    fx = poly1d(fit)
    estimated = map(fx, x)
    rmse = sqrt(sum(map(lambda (e, x, w): w * ((e - x) ** 2), zip(estimated, y, weights)))
                /len(estimated))
    future_x = date_to_int(day)
    return fx(future_x), rmse, estimated, fx, weights
