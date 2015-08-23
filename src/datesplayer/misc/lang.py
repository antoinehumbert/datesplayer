# -*- coding: utf-8 -*-
__author__ = 'Antoine Humbert'

import os
import locale
import gettext
from plyer.utils import platform



def get_default_locale():
    """
    :return: The default user's locale
    """
    if platform == 'android':
        from jnius import autoclass
        jlocale = autoclass('java.util.Locale')
        return jlocale.getDefault().toString()
    return locale.getdefaultlocale()[0]



class _(unicode):
    """ Class for internationalized strings """
    observers = []
    lang = None

    def __new__(cls, s, *args, **kwargs):
        if _.lang is None:
            _.switch_lang(get_default_locale().split('_')[0])
        s = _.translate(s, *args, **kwargs)
        return super(_, cls).__new__(cls, s)

    @staticmethod
    def translate(s, *args, **kwargs):
        return _.lang(s).format(args, kwargs)

    @staticmethod
    def bind(**kwargs):
        _.observers.append(kwargs['_'])

    @staticmethod
    def switch_lang(lang):
        # get the right locales directory, and instanciate a gettext
        locale_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.join(__file__))), 'i18n')
        locales = gettext.translation('messages', locale_dir, languages=[lang])
        _.lang = locales.ugettext

        # update all the kv rules attached to this text
        for callback in _.observers:
            callback()