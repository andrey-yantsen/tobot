from tornado import locale
from tornado.locale import Locale
from copy import deepcopy


class pgettext:
    def __init__(self, context, message):
        self._context = context
        self._message = message
        self._locale = None
        self._format_args = ()
        self._format_kwargs = ()

    @property
    def locale(self):
        if not self._locale:
            self._locale = locale.get('en_US')
        return self._locale

    @locale.setter
    def locale(self, l: Locale):
        self._locale = l

    def __str__(self):
        ret = self.locale.pgettext(self._context, self._message)
        return self._apply_format(ret)

    def _apply_format(self, text):
        if len(self._format_args) > 0:
            text = text.format(*set_locale_recursive(self._format_args, self._locale))
        if len(self._format_kwargs) > 0:
            text = text.format(**set_locale_recursive(self._format_kwargs, self._locale))
        return text

    def format(self, *args, **kwargs):
        self._format_args = deepcopy(args)
        self._format_kwargs = deepcopy(kwargs)
        return self


class npgettext(pgettext):
    def __init__(self, context, message, plural_message, count):
        super().__init__(context, message)
        self._plural_message = plural_message
        self._count = count

    def __str__(self):
        ret = self.locale.pgettext(self._context, self._message, self._plural_message, self._count)
        return self._apply_format(ret)


def set_locale_recursive(data, l):
    data = deepcopy(data)
    if isinstance(data, dict):
        for k, v in data.items():
            data[k] = set_locale_recursive(v, l)
    elif type(data) is list:
        for k, v in enumerate(data):
            data[k] = set_locale_recursive(v, l)
    elif type(data) is tuple:
        data = tuple([set_locale_recursive(v, l) for v in data])
    elif isinstance(data, pgettext):
        data.locale = l
        return str(data)
    return data
