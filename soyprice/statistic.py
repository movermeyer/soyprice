from numpy import polyfit, poly1d, sqrt
from datetime import datetime
import numpy as np


def date_to_int(dt):
    return int(dt.toordinal())


def int_to_date(number):
    return datetime.fromordinal(number)


class Regression(object):

    def __init__(self, date_list, day, variables=[]):
        self.date_list = date_list
        self.day = day
        self.variables = variables
        self.should_show_xticks = False

    @property
    def future_x(self):
        return date_to_int(self.day)

    def get_data(self, variable):
        data = filter(lambda d: d[1], variable.get(self.date_list))
        if not data:
            return [0.], [0.], [datetime.now().date()]
        x, y = zip(*data)
        x_int = map(date_to_int, x)
        return x_int, list(y), x

    def weights(self, x):
        if len(x) <= 1:
            return [1]
        return map(lambda xi: 1, x)

    @property
    def degree(self):
        return 2

    def pattern(self):
        x, y, dt = self.data
        weights = self.weights(x)
        fit = polyfit(x, y, self.degree, w=weights, full=True)[0]
        fx = poly1d(fit)
        estimated = map(fx, x)
        rmse = sqrt(sum(map(lambda (e, x, w): w * ((e - x) ** 2),
                            zip(estimated, y, weights)))
                    / len(estimated))
        return fx, estimated, rmse

    @property
    def data(self):
        if not hasattr(self, '_data'):
            self._data = self.get_data(self.variables[0])
        return self._data

    def check(self):
        pass

    def resume(self):
        self.check()
        x, y, dt = self.data
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
        return 3

    def weights(self, x):
        if len(x) <= 1:
            return [1.]
        p = lambda xi: (xi - x[0])/float(x[-1] - x[0])
        return map(lambda xi: p(xi) if p(xi) > 0.15 else 0.15, x)

    def check(self):
        if len(self.variables) is not 1:
            raise Exception('TimeRegression should have only 1 variable.')

    @property
    def x_label(self):
        x, y, dt = self.data
        return "ventana de %i dias" % (x[-1] + 1 - x[0])


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
    def data(self):
        self.should_show_xticks = True
        if not hasattr(self, '_data'):
            get_var = lambda vi: dict(zip(*(self.get_data(
                self.variables[vi])[:-1])))
            var_x, var_y = get_var(0), get_var(1)
            keys = filter(lambda k: k in var_y.keys(), var_x.keys())
            make_tuple = lambda k: [var_x[k], var_y[k], k]
            elements = zip(*map(make_tuple, keys))
            empty = [[0.], [0.], [datetime.now().date()]]
            data = map(list, elements) if len(elements) > 0 else empty
            self._data = data
        return self._data

    @property
    def future_x(self):
        x, y, dt = self.data
        return x[-1]

    def check(self):
        if len(self.variables) is not 2:
            raise Exception('VariableRegression should have always '
                            '2 variables.')

    @property
    def x_label(self):
        x, y, dt = self.data
        return "%i valores de muestra" % len(x)

    def pearson_correlation(self):
        x, y, dt = self.data
        X, Y = np.array(x), np.array(y)
        ''' Compute Pearson Correlation Coefficient. '''
        # Normalise X and Y
        X -= X.mean(0)
        Y -= Y.mean(0)
        # Standardise X and Y
        X /= X.std(0)
        Y /= Y.std(0)
        # Compute mean product
        return (np.mean(X*Y) ** 2) * 100
