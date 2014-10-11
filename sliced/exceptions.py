# -*- coding: utf-8 -*-
class OptionNotFound(KeyError):

    """
    Similar to KeyNotFound, but displays the list of valid keys
    """

    def __init__(self, message, errors={}):
        """
        message can be a string containing the value or can be a dictionary
        containing the following keys:
            value (str): the value that wasn't found
            options ([str[, str]...]): list of valid options
        """
        self.message = KeyError.__init__(self, message)

    def show_options(self):
        value = self.error.get('value', 'None')
        options = self.error.get('options', [])
        if options:
            mesg = ', '.join(map(repr, options[:-1]))
            if len(options) > 1:
                mesg += ' or ' + options[-1]
            return '{!r}\nValid options: {}.'.format(value, mesg)

    def show(self):
        if isinstance(self.message, dict):
            if 'value' in self.errors and 'options' in self.errors:
                options = self.show_options()
                return '{!r}\n{}'.format(self.message, options)
        return self.message


class DuplicateItemsNotAllowed(Exception):

    def __init__(self, message, error=None):
        Exception.__init__(self, message)
        self.message = message
        self.error = {} if error is None else error

    def show_duplicates(self):
        values = set(self.error.get('values', ['None']))
        mesg = ', '.join(map(repr, values[:-1]))
        if len(values) > 1:
            mesg += ' and ' + values[-1]
        return 'DuplicateItems:({!r})'.format(mesg)

    def show(self):
        if isinstance(self.message, dict):
            if 'values' in self.errors:
                return '{!r}\n{}'.format(self.message, show_duplicates())
        return self.message


class InvalidSliceString(Exception):

    def __init__(self, message='', info=None):
        """
        message keys:
            mesg (str):   error message
            column (int): position in text where error first occured
            width (int):  maximum width of displayed text (default 40)
        """
        Exception.__init__(self, message)
        self.message = message
        self.info = info

    def show(self):
        name = self.__class__.__name__
        if isinstance(self.info, dict):
            text = self.info.get('text', '')
            pointer = column = self.info.get('column', 0)
            max_width = self.info.get('width', 40)
            half_width = max_width//2
            if pointer > max_width:
                text = text[pointer - half_width:pointer + half_width]
                pointer -= (pointer - half_width)
            pointer = ' ' * (pointer + 1) + '^'
            print(text[:max_width])
            print(pointer)
            error_mesg = self.message if self.message else '{}: Bad syntax'.format(name)
            print('{} at column {}'.format(error_mesg, column + 1))
        else:
            print(self.message if self.message else name)
