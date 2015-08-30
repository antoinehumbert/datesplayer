# -*- coding: utf-8 -*-
__author__ = 'Antoine'

import datetime

from plyer.utils import platform

from .lang import get_default_locale, _

__all__ = ('Date', 'DateTime', 'get_holidays')



class _Base(object):
    """ Base class for "extended" date and datetime classes """

    @classmethod
    def from_native(cls, native_obj):
        ''' Return an instance of the _Android object corresponding to given native object '''
        raise NotImplementedError

    def __add__(self, other):
        return self.from_native(super(_Base, self).__add__(other))

    def __radd__(self, other):
        return self.from_native(super(_Base, self).__radd__(other))

    def __sub__(self, other):
        return self.from_native(super(_Base, self).__sub__(other))

    def __rsub__(self, other):
        return self.from_native(super(_Base, self).__rsub__(other))



class _BaseDate(_Base, datetime.date):
    """ Extend the native datetime.date class with usefull methods """

    @classmethod
    def from_native(cls, native_obj):
        ''' Return an instance of current class from a datetime.date object
        :param native_obj: a datetime.date object
        :return: instance of current class
        '''
        return cls(native_obj.year, native_obj.month, native_obj.day)

    @classmethod
    def last_date_of_year(cls, year, isoweekday=None):
        """ Return the last date of given year that is the given isoweekday (or the "real" last day of year if None)
        :param int year: the year
        :type isoweekday: int or None
        :param isoweekday: the isoweekday
        :return: instance of last date of year corresponding ot isoweekday
        """
        last_date = cls(year, 12, 31)
        if isoweekday is not None:
            last_isoweekday = last_date.isoweekday()
            if last_isoweekday >= isoweekday:
                return last_date - datetime.timedelta(days=last_isoweekday - isoweekday)
            else:
                return last_date - datetime.timedelta(days=7 + last_isoweekday - isoweekday)
        return last_date

    @classmethod
    def first_date_of_year(cls, year, isoweekday):
        """ Return the first date of given year that is the given isoweekday (or the "real" first day of year if None)
        :param int year: the year
        :type isoweekday: int or None
        :param isoweekday: the isoweekday
        :return: instance of first date of year corresponding to isoweekday
        """
        first_date = cls(year, 1, 1)
        if isoweekday is not None:
            first_isoweekday = first_date.isoweekday()
            if first_isoweekday <= isoweekday:
                return first_date + datetime.timedelta(days=isoweekday - first_isoweekday)
            else:
                return first_date + datetime.timedelta(days=7 - (first_isoweekday - isoweekday))
        return first_date

    @classmethod
    def new_year_s_day(cls, year):
        """
        :param year: the year
        :return: instance of new year's day date for given year
        """
        return cls(year, 1, 1)

    @classmethod
    def easter_sunday(cls, year):
        """ Return the easter sunday date for given year
        :param int year: the year
        :return: instance of easter sunday date for given year
        """
        golden = year % 19 # golden year - 1
        offset = 0 # offset
        century = year / 100 # century
        hem = (century - century / 4 - (8 * century + 13) / 25 + 19 * golden + 15) % 30 # hem is (23 - Epact) mod 30
        # number of days from March 21 to Paschal Full Moon
        nbr = hem - (hem / 28) * (1 - (hem / 28) * (29 / (hem + 1)) * ((21 - golden) / 11))
        # weekday for Paschal Full Moon (0=Sunday)
        week_day = (year + year / 4 + nbr + 2 - century + century / 4) % 7
        # number of days from March 21 to Sunday on or before Paschal Full Moon pascal can be from -6 to 28
        pascal = nbr - week_day + offset
        day = 1 + (pascal + 27 + (pascal + 6) / 40) % 31
        month = 3 + (pascal + 26) / 30
        return cls(year, month, day)

    @classmethod
    def easter_monday(cls, year):
        """
        :param year: the year
        :return: instance of easter monday date for given year
        """
        return cls.easter_sunday(year) + datetime.timedelta(days=1)

    @classmethod
    def labor_day(cls, year):
        """
        :param year: the year
        :return: intance of labor day date for given year
        """
        return cls(year, 5, 1)

    @classmethod
    def wwii_victory(cls, year):
        """
        :param year: the year
        :return: instance of Second World War Victory day date for given year
        """
        return cls(year, 5, 8)

    @classmethod
    def ascension_thursday(cls, year):
        """
        :param year: the year
        :return: instance of Ascension Thursday date for given year
        """
        return cls.easter_sunday(year) + datetime.timedelta(days=39)

    @classmethod
    def whit_monday(cls, year):
        """
        :param year: the year
        :return: instance of Whit Monday date for given year
        """
        return cls.easter_sunday(year) + datetime.timedelta(days=50)

    @classmethod
    def french_national_holiday(cls, year):
        """
        :param year: the year
        :return: instance of French National Holiday date for given year
        """
        return cls(year, 7, 14)

    @classmethod
    def assumption(cls, year):
        """
        :param year: the year
        :return: instance of Assumption date for given year
        """
        return cls(year, 8, 15)

    @classmethod
    def toussaint(cls, year):
        """
        :param year: the year
        :return: instance of Toussaint date for given year
        """
        return cls(year, 11, 1)

    @classmethod
    def wwi_armistice(cls, year):
        """
        :param year: the year
        :return: instance of First World War Armistice date for given year
        """
        return cls(year, 11, 11)

    @classmethod
    def christmas(cls, year):
        """
        :param year: the year
        :return: instance of Christmas day date for given year
        """
        return cls(year, 12, 25)

    def replace_weekday(self, weekday):
        ''' Return a date with same year and week and given day of week, where Monday is 0 and Synday is 6
        :param int weekday: The new weekday value (between 0 and 6)
        '''
        assert(0 <= weekday <= 6, 'Weekday must be between 0 (Monday) and 6 (Sunday)')
        return self + datetime.timedelta(days=weekday - self.weekday())

    def day_of_year(self):
        if self.year < 1900: # cannot use strftime
            day = self.replace(year=1999).day_of_year() # 1999 is not leap year
            if self.month > 2: # manage leap year
                if (datetime.date(self.year, 3, 1) - datetime.timedelta(days=1)) == 29:
                    day += 1
            return day
        return int(self.strftime('%j'))


class _BaseDateTime(_BaseDate, datetime.datetime):
    """ Extend the native datetime.datetime class with usefulle methods """

    @classmethod
    def from_native(cls, native_obj):
        ''' Return an instance of _AndroidDate from a datetime.datetime object
        :param native_obj: a datetime.datetime object
        :return: instance of _AndroidDateTime
        '''
        return cls(native_obj.year, native_obj.month, native_obj.day, native_obj.hour, native_obj.minute,
                   native_obj.second, native_obj.microsecond, native_obj.tzinfo)

    def date(self):
        ''' Get the date part of the _BaseDateTime, as a _BaseDate instance
        :return: _BaseDate corresponding to date part of the _BaseDateTime
        '''
        return _BaseDate.from_native(super(_BaseDateTime, self).date())



if str(platform) == 'android':
    from jnius import autoclass
    JvSimpleDateFormat = autoclass('java.text.SimpleDateFormat')

    class _AndroidBaseDateTime(object):
        """ A DateTime base class for Android where functions using localization (such as strftime) are overriden to use the Java
         localization, since python locale is always (None, 'C') on android and cannot be modified """

        _PY_DIRECTIVES_TO_JV = {'a': 'EEE', # Weekday as locale's abbreviated name
                                'A': 'EEEE', # Weekday as locale's full name
                                'b': 'MMM', # Month as locale’s abbreviated name
                                'B': 'MMMM', # Month as locale’s full name
                                'c': JvSimpleDateFormat.getDateTimeInstance(JvSimpleDateFormat.FULL,
                                                                            JvSimpleDateFormat.MEDIUM),
                                    # Locale’s appropriate date and time representation
                                'x': JvSimpleDateFormat.getDateInstance(JvSimpleDateFormat.MEDIUM),
                                    # Locale’s appropriate date representation
                                'X': JvSimpleDateFormat.getTimeInstance(JvSimpleDateFormat.MEDIUM)
                                    # Locale’s appropriate time representation
                                }

        def _py_to_jv_format(self, format):
            ''' Convert given python datetime string format to java SimpleDateFormat pattern
            :param format: the date format string
            :return: list of JvSimpleDateFormat instances or None (if no locale's directive are present in the format string)
            '''
            formatters = []
            pattern = ''
            has_directive = False
            is_directive = False
            for letter in format:
                if letter == '%':
                    if is_directive: # %%
                        pattern += '%'
                    else:
                        is_directive = has_directive = True # start directive
                else:
                    if is_directive:
                        formatter = self._PY_DIRECTIVES_TO_JV[letter]
                        if not isinstance(formatter, basestring):
                            if pattern:
                                formatters.append(JvSimpleDateFormat(pattern))
                                pattern = ''
                            formatters.append(formatter)
                        else:
                            pattern += formatter
                        is_directive = False
                    else:
                        if letter == "'": # escape single quote
                            pattern += "''"
                        elif letter.isalpha(): # escape letter
                            pattern += "'{}'".format(letter)
                        else:
                            pattern += letter
            if pattern:
                formatters.append(JvSimpleDateFormat(pattern))
            return formatters if has_directive else None

        def _apply_unlocalized_directives(self, format):
            """ Return a new format string after applying locale's independent directives
            :param format: the date format string
            :return: a new date format string with locale's independent directives applied
            """
            new_format = ''
            is_directive = False
            for letter in format:
                if is_directive:
                    if letter == '%':
                        new_format += '%%' # will result in %% after applying first formatting
                    elif letter in self._PY_DIRECTIVES_TO_JV:
                        new_format += '%' # escape directives so that it results in the directive itself
                    is_directive = False
                else:
                    if letter == '%':
                        is_directive = True
                new_format += letter
            return super(_AndroidBaseDateTime, self).strftime(new_format)

        def _apply_localized_directives(self, format):
            """ Return a string representing the date according to given string format which contains only locale's
                dependent directives.
            :param format: the date format string
            :return: str
            """
            JvCalendar = autoclass('java.util.Calendar')
            jv_calendar = JvCalendar.getInstance();
            jv_calendar.set(self.year, self.month - 1, self.day, getattr(self, 'hour', 0), getattr(self, 'minute', 0),
                            getattr(self, 'second', 0))
            jv_calendar.set(JvCalendar.MILLISECOND, getattr(self, 'microsecond', 0) / 1000)
            formatters = self._py_to_jv_format(format)
            if formatters is None:
                return format
            return ''.join((formatter.format(jv_calendar.getTime()) for formatter in formatters))

        def strftime(self, format):
            """ Return a string reprsenting the date according to given string format
            :param format: the date format string
            :return: str
            """
            new_format = self._apply_unlocalized_directives(format)
            return self._apply_localized_directives(new_format)



    class _AndroidDate(_AndroidBaseDateTime, _BaseDate): # Take care of order for MRO
        """ A Date for Android where functions using localization (such as strftime) are overriden to use the Java
         localization, since python locale is always (None, 'C') on android and cannot be modified """
        pass



    class _AndroidDateTime(_AndroidBaseDateTime, _BaseDateTime): # Take care of order for MRO
        """ A DateTime for Android where functions using localization (such as strftime) are overriden to use the Java
         localization, since python locale is always (None, 'C') on android and cannot be modified """

        def date(self):
            ''' Get the date part of the _AndroidDateTime, as a _AndroidDate instance
            :return: _AndroidDate corresponding to date part of the _AndroidDateTime
            '''
            return _AndroidDate.from_native(super(_AndroidBaseDateTime, self).date())



    Date = _AndroidDate
    DateTime = _AndroidDateTime
else:
    Date = _BaseDate
    DateTime = _BaseDateTime


HOLIDAYS = {'FR': {_("New Year's day"): Date.new_year_s_day,
                   _("Easter Monday"): Date.easter_monday,
                   _("Labor day"): Date.labor_day,
                   _("WWII Victory"): Date.wwii_victory,
                   _("Ascension Thursday"): Date.ascension_thursday,
                   _("Whit Monday"): Date.whit_monday,
                   _("National Holiday"): Date.french_national_holiday,
                   _("Assumption"): Date.assumption,
                   _("Toussaint"): Date.toussaint,
                   _("WWI Armistice"): Date.wwi_armistice,
                   _("Christmas"): Date.christmas}
            }

def get_holidays(year, locale=None):
    """ Return holidays for given year and given locale (default to user default locale)
    :param year: the year
    :param locale: the locale to use (or just the country part of the locale)
    :return: A dictionary of holidays for given year and locale
    """
    if locale is None:
        locale = get_default_locale()
    holidays = HOLIDAYS.get(locale.split('_')[-1])
    if holidays is not None:
        return dict((name, func(year)) for name, func in holidays.iteritems())
    return {}
