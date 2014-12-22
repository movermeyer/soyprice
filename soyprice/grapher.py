from scraper import date_to_int
import pylab as pl
from statistic import forecast


class Graph(object):

    def __init__(self):
        self.variables = []

    def add(self, variable):
        self.variables.append(variable)

    def create_figure(self):
        pl.figure(figsize=(8, 4), dpi=100)
        pl.suptitle('forecasted by @limiear', y=0.05)

    def put_data_in_figure(self, variable, date_list, day):
        price, rmse, fix, fx, weights = forecast(variable, date_list, day)
        data = filter(lambda d: d[1], variable.get(date_list))
        x, y = zip(*data)
        x = map(date_to_int, x)
        next_x = date_to_int(day)
        next_y = fx(next_x)
        border = 2
        ratio = max(y) * 0.05
        x_values = list(x) + [next_x]
        y_values = list(y) + [next_y]
        limits = (min(x_values) - border,
                  max(x_values) + border,
                  min(y_values) - border * ratio,
                  max(y_values) + border * ratio)
        sp = pl.subplot(1, 1, 1)
        sp.axis(limits)
        sp.set_title(variable.description)
        sp.scatter(x, y, marker=".", linewidth=0.5)
        w_s = lambda w: 1/(w if w > 0 else 0.001)
        sp.plot(x, map(lambda (x, w): x - (rmse * w_s(w)), zip(fix, weights)),
                color="green", linewidth=1.0, linestyle="--",)
        sp.plot(x, fix, color="red", linewidth=1.0, linestyle="-",)
        sp.plot(x, map(lambda (x, w): x + (rmse * w_s(w)), zip(fix, weights)),
                color="green", linewidth=1.0, linestyle="--",)
        sp.plot([next_x], [next_y], color="red", marker="o")
        pl.xticks([], 0, endpoint=True)
        sp.yaxis.tick_right()
        sp.yaxis.set_label_position("right")
        sp.yaxis.label.set_text(variable.reference)
        sp.yaxis.label.set_size(10)
        sp.set_xlabel("%i days window" % (x[-1] + 1 - x[0]), fontsize=10)

    def save_figure(self, variable, filename):
        index = self.variables.index(variable)
        g = filename.split('.')
        filename = '%s_%i.%s' % ('.'.join(g[:-1]), index, g[-1])
        pl.savefig(filename, dpi=100)
        return filename

    def save_variable(self, variable, date_list, day, filename):
        self.create_figure()
        self.put_data_in_figure(variable, date_list, day)
        return self.save_figure(variable, filename)

    def save(self, date_list, day, filename):
        return map(lambda v: self.save_variable(v, date_list, day, filename),
                   self.variables)


def draw(variables, date_list, day, filename):
    graph = Graph()
    list(map(graph.add, variables))
    return graph.save(date_list, day, filename)
