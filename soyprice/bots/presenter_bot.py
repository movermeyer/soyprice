# -*- coding: utf-8 -*-
from twython import Twython, TwythonError
from scraper import get_days, get_next_workable_day
from statistic import TimeRegression, VariableRegression, int_to_date
from grapher import draw
import time
from twitter_keys import APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET
from core import Variable
from StringIO import StringIO
from variables.core import app
from datetime import datetime, timedelta


def twython(func):
    def func_wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except TwythonError as e:
            print e
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
        self.date_list = get_days(datetime.today(),
                                  range(0, amount))
        self.date_list.reverse()
        self.day = get_next_workable_day(self.date_list[-1])

    def upload_media(self, image):
        with open(image, 'rb') as photo:
            result = StringIO(photo.read())
        return result

    def tweet(self, status, images):
        # time.sleep(10)
        template = "%s #soyprice"
        """
        if not images:
            self.twitter.update_status(status=template % status)
        else:
            medias = map(lambda i: self.upload_media(i), images)
            self.twitter.post('/statuses/update_with_media',
                              params={'status': template % status,
                              'media': medias[0]})
                              """
        print template % status, len(template % status)

    @twython
    def dollar_showcase(self):
        dollars = Variable('dollar/blue')
        regression = TimeRegression(self.date_list, self.day, [dollars])
        fx, _, rmse = regression.pattern()
        price = fx(regression.future_x)
        filename = draw(regression, 'graph_dollar.png')
        print self.day, price, rmse, filename
        self.tweet(('Estimación Dollar Blue para el %s: AR$ %.2f '
                    '(RMSE: AR$ %.2f)') %
                   (self.day.strftime('%d-%m-%Y'), price, int(rmse)), filename)

    @twython
    def soy_showcase(self):
        # sanmartin
        sanmartin = Variable('soy/afascl')
        rosario = Variable('soy/bcr')
        chicago = Variable('soy/chicago')
        # foorecast soy sanmartin
        regression = TimeRegression(self.date_list, self.day, [rosario])
        fx, _, rmse = regression.pattern()
        price = fx(regression.future_x)
        filename = draw(regression, 'graph_soy_rosario.png')
        self.tweet(('Estimación Soja Rosario para el'
                    ' %s: AR$ %.f (RMSE: AR$ %.f)') %
                   (self.day.strftime('%d-%m-%Y'), price, rmse), filename)
        regression = TimeRegression(self.date_list, self.day, [chicago])
        fx, _, rmse = regression.pattern()
        price = fx(regression.future_x)
        filename = draw(regression, 'graph_soy_chicago.png')
        self.tweet(('Estimación Soja Chicago para el'
                    ' %s: U$D %.f (RMSE: U$D %.f)') %
                   (self.day.strftime('%d-%m-%Y'), price, rmse), filename)
        regression = TimeRegression(self.date_list, self.day, [sanmartin])
        fx, _, rmse = regression.pattern()
        price = fx(regression.future_x)
        filename = draw(regression, 'graph_soy_sanmartin.png')
        self.tweet(('Estimación Soja puerto San Martín con descarga para el'
                    ' %s: AR$ %.f (RMSE: AR$ %.f)') %
                   (self.day.strftime('%d-%m-%Y'), price, rmse), filename)
        regression = VariableRegression(self.date_list,
                                        self.day, [chicago, sanmartin])
        fx, _, rmse = regression.pattern()
        filename = draw(regression, 'graph_soy_related.png')
        price = fx(regression.future_x)
        x, y, dt = regression.data
        pearson = regression.pearson_correlation()
        m_dt = max(dt)
        m_dt = int_to_date(m_dt) if isinstance(m_dt, int) else m_dt
        self.tweet(('Correlación Soja Chicago con pto. San Martín hasta el'
                    ' %s: AR$ %.f (RMSE: AR$ %.f, Pearson: %.2f%%)') %
                   (m_dt.strftime('%d-%m-%Y'), price, rmse, pearson),
                   filename)
        self.tweet('El código puede ser descargado desde https://github.com/limiear/soyprice.', [])

    def demonstrate(self):
        self.dollar_showcase()
        self.soy_showcase()


dt = datetime.now() + timedelta(minutes=2)
@app.run_every("day", dt.strftime("%H:%M"))
def run():
    presenter = Presenter()
    presenter.demonstrate()
