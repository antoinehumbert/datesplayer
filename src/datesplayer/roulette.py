# -*- coding: utf-8 -*-
''' Define a new Slot class for displaying month names'''

import datetime
from kivy.garden.roulette import CyclicSlot, CyclicRoulette
from kivy.properties import NumericProperty, StringProperty, ObjectProperty, AliasProperty, ListProperty
from misc.date import Date, DateTime



class ItemsCyclicSlot(CyclicSlot):

    names = ListProperty([])

    def value_str(self, value):
        real_value = value - (0 if self.zero_indexed else 1)
        if real_value == 0:
            return '--'
        return self.names[real_value - 1]

class ItemsCyclicRoulette(CyclicRoulette):
    """ A roulette initialized with (display name, value) items """

    tick_cls = ItemsCyclicSlot
    items = ObjectProperty(None)
    values = ObjectProperty(None)

    def on_items(self, *args):
        if self.items is None:
            self.values = []
            self.cycle = 1
            if self.tick:
                self.tick.names = []
        else:
            names, self.values = zip(*self.items)
            self.cycle = len(self.items) + 1
            if self.tick:
                self.tick.names = names

    def get_value(self):
        real_index = self.selected_value - (0 if self.zero_indexed else 1)
        if real_index == 0:
            return None
        else:
            return self.values[real_index - 1]

    def set_value(self, value):
        try:
            index = self.values.index(value)
        except ValueError:
            self.selected_value = 0 if self.zero_indexed else 1
        else:
            self.selected_value = index + (1 if self.zero_indexed else 2)

    value = AliasProperty(get_value, set_value, bind=['selected_value'])



class MonthCyclicSlot(CyclicSlot):

    def value_str(self, value):
        offset = 1 if self.zero_indexed else 0
        return DateTime.strptime(str(value + offset), '%m').strftime('%B')



class WeekdayCyclicSlot(CyclicSlot):

    def value_str(self, value):
        offset = 0 if self.zero_indexed else -1
        return DateTime.strptime('200001{}'.format(value + offset), '%Y%W%w').strftime('%A')



class WeekCyclicSlot(CyclicSlot):

    max_year_week = NumericProperty(None)
    max_prev_year_week = NumericProperty(None)
    year = NumericProperty(None)
    year_format_str = StringProperty('{}')
    offset = NumericProperty(None)

    def on_year(self, *args):
        self.max_year_week = Date.last_date_of_year(self.year, 4).isocalendar()[1]
        self.max_prev_year_week = Date.last_date_of_year(self.year - 1, 4).isocalendar()[1]

    def value_str(self, value):
        week = value + self.offset + (0 if self.zero_indexed else 1)
        if self.year:
            if week == 0:
                return '-'.join((self.year_format_str.format(self.year - 1),
                                 self.format_str.format(self.max_prev_year_week)))
            elif week > self.max_year_week:
                return '-'.join((self.year_format_str.format(self.year + 1), self.format_str.format(1)))
        return self.format_str.format(week)



class WeekCyclicRoulette(CyclicRoulette):

    tick_cls = ObjectProperty(WeekCyclicSlot)
    year_format_str = StringProperty('{}')
    date = ObjectProperty(None)
    offset = NumericProperty(0)

    def on_tick(self, *args):
        super(WeekCyclicRoulette, self).on_tick(*args)
        tick = self.tick
        if tick:
            tick.year = self.year
            tick.year_format_str = self.year_format_str

    def on_date(self, *args):
        first_week = Date.first_date_of_year(self.date.year, self.date.isoweekday()).isocalendar()[1]
        last_week = Date.last_date_of_year(self.date.year, self.date.isoweekday()).isocalendar()[1]
        min_week = first_week if first_week <= 2 else 0 # 0 is for last week of preceding year
        max_week = Date.last_date_of_year(self.date.year, 4).isocalendar()[1] + 1 if last_week == 1 else last_week
        isoyear, isoweek, _ = self.date.isocalendar()
        if isoyear < self.date.year:
            isoweek = 0
        elif isoyear > self.date.year:
            isoweek = max_week
        self.cycle = max_week - min_week + 1
        self.offset = min_week
        self.selected_value = isoweek - self.offset

    def on_selected_value(self, *args):
        if self.date is not None:
            week = self.selected_value - (0 if self.zero_indexed else 1)
            self.date = (Date.first_date_of_year(self.date.year, self.date.isoweekday()) +
                         datetime.timedelta(days=7 * week))

    def get_year(self):
        return self.date.year if self.date is not None else None

    year = AliasProperty(get_year, bind=['date'])

    def on_year(self, *args):
        if self.tick:
            self.tick.year = self.year

    def on_year_format_str(self, *args):
        if self.tick:
            self.tick.year_format_str = self.year_format_str

    def on_offset(self, *args):
        if self.tick:
            self.tick.offset = self.offset
