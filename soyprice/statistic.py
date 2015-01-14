from numpy import polyfit, poly1d, sqrt


def date_to_int(dt):
    return int(dt.toordinal())


class Regression(object):

    def __init__(self, date_list, day, variables=[]):
        self.date_list = date_list
        self.day = day
        self.variables = variables

    @property
    def future_x(self):
        return date_to_int(self.day)

    def get_data(self, variable):
        data = filter(lambda d: d[1], variable.get(self.date_list))
        if data is []:
            return [0.], [0.]
        x, y = zip(*data)
        x = map(date_to_int, x)
        return x, list(y)

    def pattern(self):
        x, y = self.get_data(self.variables[0])
        weights = self.weights(x)
        fit = polyfit(x, y, self.degree, w=weights)
        fx = poly1d(fit)
        estimated = map(fx, x)
        rmse = sqrt(sum(map(lambda (e, x, w): w * ((e - x) ** 2),
                            zip(estimated, y, weights)))
                    / len(estimated))
        return fx, estimated, rmse

    def check(self):
        pass

    def resume(self):
        self.check()
        x, y = self.data
        fx, estimated, rmse = self.pattern()
        next_x = self.future_x
        next_y = fx(next_x)
        return x, y, estimated, self.weights(x), rmse, next_x, next_y


class TimeRegression(Regression):

    @property
    def description(self):
        return self.variables[0].description

    @property
    def reference(self):
        return self.variables[0].reference

    @property
    def degree(self):
        return 2

    @property
    def data(self):
        return self.get_data(self.variables[0])

    def weights(self, x):
        if len(x) <= 1:
            return [1]
        return map(lambda xi: (xi - x[0])/float(x[-1] - x[0]), x)

    def check(self):
        if len(self.variables) is not 1:
            raise Exception('TimeRegression should have only 1 variable.')


class VariableRegression(Regression):

    @property
    def description(self):
        descriptions = map(lambda v: v.description, self.variables)
        return ' vs. '.join(descriptions)

    @property
    def reference(self):
        return ''

    @property
    def degree(self):
        return 1

    @property
    def future_x(self):
        return self.data[0][-1]

    @property
    def data(self):
        get_var = lambda vi: dict(zip(*(self.get_data(self.variables[vi]))))
        var_x, var_y = get_var(0), get_var(1)
        keys = filter(lambda k: k in var_y.keys(), var_x.keys())
        make_pair = lambda k: [var_x[k], var_y[k]]
        elements = zip(*map(make_pair, keys))
        return map(list, elements)

    def weights(self, x):
        if len(x) <= 1:
            return [1]
        return map(lambda xi: 1, x)

    def check(self):
        if len(self.variables) is not 2:
            raise Exception('VariableRegression should have always 2 variables.')
