from numpy import polyfit, poly1d, sqrt

def forecast(x, y, future_x):
    fit = polyfit(x, y, 6)
    fx = poly1d(fit)
    estimated = map(fx, x)
    rmse = sqrt(sum(map(lambda (e, x): (e - x) ** 2, zip(estimated, y)))
                /len(estimated))
    return fx(future_x), rmse, estimated, fx
