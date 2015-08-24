# *-* coding: utf-8 -*-
'''The main loop file of the kivy app.'''

__author__ = "Antoine Humbert"
__copyright__ = ""
__credits__ = []

__license__ = "MIT"
__version__ = "0.1.0"
__maintainer__ = "Antoine Humbert"
__email__ = "antoine.humbert@gmail.com"
__status__ = "Prototype"

import kivy
kivy.require("1.9.0")

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, AliasProperty

import datetime
import locale
from misc.date import Date, DateTime, get_holidays


def max_day_of_month(date):
    next_month = date.replace(day=28) + datetime.timedelta(days=4)
    return (next_month - datetime.timedelta(days=next_month.day)).day



class DatesPlayer(BoxLayout):
    '''This is the DatesPlayer application layout class'''

    date = ObjectProperty(Date.today())
    weekday_roulette = ObjectProperty(None)
    week_roulette = ObjectProperty(None)
    day_of_year_roulette = ObjectProperty(None)
    notable_days_roulette = ObjectProperty(None)
    year_roulette = ObjectProperty(None)
    month_roulette = ObjectProperty(None)
    day_roulette = ObjectProperty(None)

    def update_roulettes(self):
        ''' Re-center roulettes on their selected_value.'''
        for roulette in (self.weekday_roulette, self.week_roulette, self.day_of_year_roulette,
                         self.notable_days_roulette, self.year_roulette, self.month_roulette, self.day_roulette):
            roulette.center(animate=False)

    @staticmethod
    def redraw_roulette(roulette):
        ''' Redraw given roulette after changing some attributes '''
        roulette.on_ticks()
        roulette.labeller.instructions = {}
        roulette.redraw()

    def get_day(self):
        return self.date.day

    def set_day(self, value):
        self.date = self.date.replace(day=value)

    day = AliasProperty(get_day, set_day, bind=['date'])

    def get_weekday(self):
        return self.date.isoweekday() % 7

    def set_weekday(self, value):
        self.date = DateTime.strptime('{}{}{}'.format(self.year, self.date.strftime('%W'), value), '%Y%W%w').date()

    weekday = AliasProperty(get_weekday, set_weekday, bind=['date'])

    def get_month(self):
        return self.date.month

    def set_month(self, value):
        max_day = max_day_of_month(datetime.date(self.year, value, 1))
        if self.day > max_day:
            self.day = max_day
        self.date = self.date.replace(month=value)

    month = AliasProperty(get_month, set_month, bind=['date'])

    def get_year(self):
        return self.date.year

    def set_year(self, value):
        if self.month == 2:
            max_day = max_day_of_month(datetime.date(value, self.month, 1))
            if self.day > max_day:
                self.day = max_day
        self.date = self.date.replace(year=value)

    year = AliasProperty(get_year, set_year, bind=['date'])

    def get_day_of_year(self):
        return int(self.date.strftime('%j'))

    def set_day_of_year(self, value):
        self.date += datetime.timedelta(days=value - self.day_of_year)

    day_of_year = AliasProperty(get_day_of_year, set_day_of_year, bind=['date'])

    def get_max_day_of_month(self):
        return max_day_of_month(self.date)

    max_day_of_month = AliasProperty(get_max_day_of_month, bind=['month'])

    def get_max_day_of_year(self):
        return 337 + (datetime.date(self.year, 3, 1) - datetime.timedelta(days=1)).day

    max_day_of_year = AliasProperty(get_max_day_of_year, bind=['year'])

    def get_notable_days(self):
        return sorted((item for item in get_holidays(self.date.year).items()), key=lambda item: item[1])

    notable_days = AliasProperty(get_notable_days, bind=['year'])

    def get_next_not_notable_day(self):
        notable_days = [item[1] for item in self.notable_days]
        next_date = self.date
        while next_date in notable_days:
            next_date += datetime.timedelta(days=1)
        return next_date



class DatesPlayerApp(App):
    '''This is the Test application main controller class'''

    def build(self):
        '''This method is used to initialize the application/

        :return:
           The main application Widget'''
        # Set locale to current user locale for displaying months and days
        locale.setlocale(locale.LC_ALL, '')
        return DatesPlayer()



if __name__ == '__main__':
    DatesPlayerApp().run()