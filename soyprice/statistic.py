from numpy import polyfit, poly1d, sqrt
from math import log, e

def forecast(x, y, future_x):
    weights = map(lambda xi: (xi -x[0])/float(x[-1] - x[0]), x)
    print weights
    fit = polyfit(x, y, 6, w=weights)
    fx = poly1d(fit)
    estimated = map(fx, x)
    rmse = sqrt(sum(map(lambda (e, x, w): w * ((e - x) ** 2), zip(estimated, y, weights)))
                /len(estimated))
    print fx(future_x)
    return fx(future_x), rmse, estimated, fx, weights
