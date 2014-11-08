from numpy import polyfit, poly1d

def forecast(x, y, future_x):
    fit = polyfit(x, y, 6)
    fx = poly1d(fit)
    return fx(future_x), map(fx, x), fx
