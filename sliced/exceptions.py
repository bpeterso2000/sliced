# -*- coding: utf-8 -*-
def show_choices(choice, choices):
    mesg = repr(choice)
    if len(choices):
        mesg = '{}\nValid options: {} or {}'
        values = ', '.join(repr(i) for i in choices[:-1])
        return mesg.format(repr(choice), values, repr(choices[-1]))
    return mesg


class InvalidIntervalType(Exception):
    def __init__(self, name, types):
        self.message = Exception.__init__(show_choices(name, types))


class UnknownDialect(Exception):
    def __init__(self, name, dialects):
        self.message = Exception.__init__(self, show_choices(name, dialects))


class EndPointZeroNotAllowed(Exception):
    def __init__(self, message):
        self.message = Exception.__init__(self, message)

class EndPointValueError(Exception):
    def __init__(self, message):
        self.message = Exception.__init__(self, message)


class InvalidStepSize(Exception):
    def __init__(self, message):
        self.message = Exception.__init__(self, message)


class OriginValueError(Exception):
    def __init__(self):
        self.message = 'Origin must be 0 or 1.'


class InvalidSliceString(Exception):
    def __init__(self, message):
        self.message = Exception.__init__(self, message)


class InvalidSeparator(Exception):
    def __init__(self, message):
        self.message = Exception.__init__(self, message)
