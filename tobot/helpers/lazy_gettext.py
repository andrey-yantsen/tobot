from tornado import locale
from tornado.locale import Locale


class pgettext:
    def __init__(self, context, message):
        self.context = context
        self.message = message
        self._locale = None
        self.format_args = ()
        self.format_kwargs = {}

    @property
    def locale(self):
        if not self._locale:
            self._locale = locale.get('en_US')
        return self._locale

    @locale.setter
    def locale(self, l: Locale):
        self._locale = l

    def __str__(self):
        ret = self.locale.pgettext(self.context, self.message)
        return self._apply_format(ret)

    def _apply_format(self, text):
        if self.format_args or self.format_kwargs:
            return text.format(*set_locale_recursive(self.format_args, self._locale),
                               **set_locale_recursive(self.format_kwargs, self._locale))
        return text

    def format(self, *args, **kwargs):
        self.format_args = args
        self.format_kwargs = kwargs
        return self


class npgettext(pgettext):
    def __init__(self, context, message, plural_message, count):
        super().__init__(context, message)
        self.plural_message = plural_message
        self.count = count

    def __str__(self):
        ret = self.locale.pgettext(self.context, self.message, self.plural_message, self.count)
        return self._apply_format(ret)


def set_locale_recursive(data, l):
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
