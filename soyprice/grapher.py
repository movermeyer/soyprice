#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pylab as pl


class Graph(object):

    def create_figure(self):
        pl.figure(figsize=(8, 4), dpi=100)
        pl.suptitle('estimado por @limiear', y=0.05)

    def draw_title(self, x, y, next_x, next_y, description):
        self.sp = pl.subplot(1, 1, 1)
        border = 2
        ratio = max(y) * 0.05
        x_values = list(x) + [next_x]
        y_values = list(y) + [next_y]
        limits = (min(x_values) - border,
                  max(x_values) + border,
                  min(y_values) - border * ratio,
                  max(y_values) + border * ratio)
        self.sp.axis(limits)
        self.sp.set_title(description)

    def draw_data(self, x, y, reference, x_label):
        self.sp.scatter(x, y, marker=".", linewidth=0.5)
        self.sp.yaxis.set_label_position("right")
        self.sp.yaxis.label.set_text(reference)
        self.sp.yaxis.label.set_size(10)
        self.sp.yaxis.tick_right()
        pl.xticks([], 0, endpoint=True)
        self.sp.set_xlabel(x_label, fontsize=10)

    def draw_rmse(self, x, weights, rmse):
        w_s = lambda w: 1/(w if w > 0 else 0.001)
        border_y = lambda b: map(lambda (x, w): x + b * rmse * w_s(w),
                                 weights)
        draw_border = lambda b: self.sp.plot(x, border_y(b), color="green",
                                             linewidth=1.0, linestyle="--",)
        draw_border(-1)
        draw_border(1)

    def draw_estimated(self, x, y, next_x, next_y):
        self.sp.plot([next_x], [next_y], color="red", marker="o")
        self.sp.plot(x, y, color="red", linewidth=1.0, linestyle="-",)

    def put_data_in_figure(self, regression):
        x, y, fix, weights, rmse, next_x, next_y = regression.resume()
        self.draw_title(x, y, next_x, next_y, regression.description)
        self.draw_data(x, y, regression.reference, regression.x_label)
        self.draw_rmse(x, zip(fix, weights), rmse)
        self.draw_estimated(x, fix, next_x, next_y)

    def save_figure(self, regression, filename):
        pl.savefig(filename, dpi=100)
        return filename

    def save(self, regression, filename):
        self.create_figure()
        self.put_data_in_figure(regression)
        return self.save_figure(regression, filename)


def draw(regression, filename):
    graph = Graph()
    return [graph.save(regression, filename)]
