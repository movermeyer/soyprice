from numpy import polyfit, poly1d

def forecast(x, y):
    fit = polyfit(x, y, 3)
    fx = poly1d(fit)
    return fx(x[0] + 1)
