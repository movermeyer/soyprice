#!/usr/bin/env python
# -*- coding: utf-8 -*-

from twython import Twython, TwythonError
import datetime
from scraper import get_days, get_next_workable_day
from statistic import forecast, TimeRegression, VariableRegression
import model.database as db
from grapher import draw
import time
from twitter_keys import *
from model import SanMartin, Chicago, BlueDollar


def twython(func):
    def func_wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except TwythonError as e:
            print e
        except Exception as e:
            pass
    return func_wrapper


class Presenter(object):

    def __init__(self):
        self.twitter = Twython(
            APP_KEY,
            APP_SECRET,
            OAUTH_TOKEN,
            OAUTH_TOKEN_SECRET
        )
        amount = 15
        self.date_list = get_days(datetime.datetime.today(),
                                  range(0, amount))
        self.date_list.reverse()
        self.day = get_next_workable_day(self.date_list[-1])

    def upload_media(self, image):
        photo = open(image, 'rb')
        return self.twitter.upload_media(media=photo)

    def tweet(self, status, images):
        time.sleep(10)
        # medias = map(lambda i: self.upload_media(i)['media_id'], images)
        template = "%s [https://github.com/limiear/soyprice]"
        # self.twitter.update_status(media_ids=medias,
        #                           status=template % status)

    @twython
    def dollar_showcase(self, cache):
        dollars = BlueDollar(cache)
        price, rmse, _, fx, weights = forecast(dollars, self.date_list,
                                                 self.day)
        filename = draw(TimeRegression, [dollars],
                        self.date_list, self.day, 'graph_dollar.png')
        self.tweet(('Forecast Dollar Blue para el %s: AR$ %.2f '
                    '(RMSE: AR$ %.2f)') %
                   (self.day.strftime('%d-%m-%Y'), price, int(rmse)), filename)

    @twython
    def soy_showcase(self, cache):
        # sanmartin
        sanmartin = SanMartin(cache)
        chicago = Chicago(cache)
        # forecast soy sanmartin
        price, rmse, _, fx, weights = forecast(chicago, self.date_list,
                                                 self.day)
        price, rmse, _, fx, weights = forecast(sanmartin, self.date_list,
                                                 self.day)
        filename = draw(TimeRegression, [chicago],
                        self.date_list, self.day, 'graph_soy_chicago.png')
        filename = draw(TimeRegression, [sanmartin],
                        self.date_list, self.day, 'graph_soy_sanmartin.png')
        # filename = draw(VariableRegression, [sanmartin, chicago],
        #                self.date_list, self.day, 'graph_soy_related.png')
        self.tweet(('Forecast Soja puerto San Martín con descarga para el'
                    ' %s: AR$ %.f (RMSE: AR$ %i)') %
                   (self.day.strftime('%d-%m-%Y'), price, int(rmse)), filename)
        self.tweet(('Forecast Soja Chicago para el'
                    ' %s: U$D %.f (RMSE: U$D %i)') %
                   (self.day.strftime('%d-%m-%Y'), price, int(rmse)), filename)

    def demonstrate(self):
        cache = db.open()
        self.dollar_showcase(cache)
        self.soy_showcase(cache)
        db.close(cache)


presenter = Presenter()
presenter.demonstrate()
