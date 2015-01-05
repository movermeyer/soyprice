from numpy import polyfit, poly1d, sqrt


def date_to_int(dt):
    return int(dt.toordinal())


def forecast(variable, date_list, day):
    data = filter(lambda d: d[1], variable.get(date_list))
    if len(data) == 0:
        return 0., 0., 0., lambda x: x, (1.)
    if len(data) == 1:
        return data[0][1], 0, [data[0][1]], lambda x: x, [1]
    x, y = zip(*data)
    x = map(date_to_int, x)
    weights = map(lambda xi: (xi - x[0])/float(x[-1] - x[0]), x)
    fit = polyfit(x, y, 6, w=weights)
    fx = poly1d(fit)
    estimated = map(fx, x)
    rmse = sqrt(sum(map(lambda (e, x, w): w * ((e - x) ** 2),
                        zip(estimated, y, weights)))
                / len(estimated))
    future_x = date_to_int(day)
    return fx(future_x), rmse, estimated, fx, weights


class Regression(object):

    def __init__(self, date_list, day):
        self.date_list = date_list
        self.day = day
        self.variables = []

    def add(self, variable):
        self.variables.append(variable)

    def get_data(self, variable):
        data = filter(lambda d: d[1], variable.get(self.date_list))
        if len(data) <= 1:
            raise Exception('No data available for %s' % variable.name)
        x, y = zip(*data)
        x = map(date_to_int, x)
        return x, list(y)


class TimeRegression(Regression):

    def do(self):
        if len(self.variables) is not 1:
            raise Exception('Invalid amount of variables for a TimeRegression.')
        variable = self.variables[0]
        price, rmse, fix, fx, weights = forecast(variable,
                                                 self.date_list, self.day)
        x, y = self.get_data(variable)
        next_x = date_to_int(self.day)
        next_y = fx(next_x)
        return x, y, fix, weights, rmse, next_x, next_y


class VariableRegression(Regression):

    def do(self):
        pass
