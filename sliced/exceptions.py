# -*- coding: utf-8 -*-
class OptionNotFound(KeyError):

    """
    Similar to KeyNotFound, but displays the list of valid keys
    """

    def __init__(self, message):
        """
        message can be a string containing the value or can be a dictionary
        containing the following keys:
            value (str): the value that wasn't found
            options ([str[, str]...]): list of valid options
        """
        self.message = KeyError.__init__(self, message)

    def display_with_available_options(self):
        """
        """
        mesg = repr(choice)
        if len(choices):

            mesg = '{}\nValid options: {} or {}'
            values = ', '.join(repr(i) for i in choices[:-1])
            return mesg.format(repr(choice), values, repr(choices[-1]))
        return mesg

    def __str__(self):
        message = self.message
        if isinstance(message, dict):
            if 'options' in message:
                return self.display_with_available_options()
            message = message['value']
        return "OptionNotFound({!r})".format(message)


class InvalidSliceString(Exception):

    def __init__(self, message):
        """
        message keys:
            mesg (str):   error message
            column (int): position in text where error first occured
            width (int):  maximum width of displayed text (default 40)
        """
        self.message = Exception.__init__(self, message)

    def _display_with_pointer_to_error(self):
        mesg = self.message['msg']
        pointer = self.message['column']
        max_width = self.message.get('width', 40)
        half_width = max_width//2
        if pointer > max_width:
            mesg = mesg[pointer - half_width:pointer + half_width]
            pointer -= (pointer - half_width)
        pointer = ' ' * (pointer + len(type(self))) + '^'
        location = 'Invalid text at column {}.'.format(self.message['column'])
        return '\n'.join(['', mesg[:max_width], pointer, location])

    def __str__(self):
        message = self.message
        if isinstance(message, dict):
            if 'mesg' in message and 'column' in message:
                return self._display_with_pointer_to_error()
        return message
