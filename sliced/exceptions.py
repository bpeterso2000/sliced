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

    def display_with_available_options(self):
        options = self.errors['options']
        mesg = ', '.join(map(repr, options[:-1]))
        if len(options) > 1:
            mesg += ' or ' + options[-1]
        return '{!r}\nValid options: {}.'.format(self.errors['value'], mesg)

    def __str__(self):
        if isinstance(self.message, dict):
            if 'value' in self.errors and 'options' in self.errors:
                options = self.display_with_available_options()
                return '{!r}\n{}'.format(self.message, options)
        return self.message


class DuplicateItemsNotAllowed(Exception):

    def __init__(self, message, errors={}):
        self.message = Exception.__init__(self, message)

    def display_with_duplicate_items(self):
        values = set(self.errors['values'])
        mesg = ', '.join(map(repr, values[:-1]))
        if len(values) > 1:
            mesg += ' and ' + values[-1]
        return 'DuplicateItems:({!r})'.format(mesg)

    def __str__(self):
        if isinstance(self.message, dict):
            if 'values' in self.errors:
                dups = self.display_with_duplicates()
                return '{!r}\n{}'.format(self.message, dups)
        return self.message


class InvalidSliceString(Exception):

    def __init__(self, message, errors):
        """
        message keys:
            mesg (str):   error message
            column (int): position in text where error first occured
            width (int):  maximum width of displayed text (default 40)
        """
        self.message = Exception.__init__(self, message)

    def _display_with_pointer_to_error(self):
        pointer = self.errors['column']
        max_width = self.errors.get('width', 40)
        half_width = max_width//2
        if pointer > max_width:
            mesg = self.message[pointer - half_width:pointer + half_width]
            pointer -= (pointer - half_width)
        pointer = ' ' * (pointer + len(type(self))) + '^'
        location = 'Invalid text at column {}.'.format(self.errors['column'])
        return '\n'.join(['', self.message[:max_width], pointer, location])

    def __str__(self):
        message = self.message
        if isinstance(message, dict):
            if 'mesg' in message and 'column' in message:
                return self._display_with_pointer_to_error()
        return message
