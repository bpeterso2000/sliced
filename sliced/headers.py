# -*- coding: utf-8 -*-
"""
Allows header names to be used in slice strings
===============================================
Converts header names to indices.
"""

import re

from pyparsing import Regex

from exceptions import InvalidSliceString


class Headers(object):

    column_names = Regex(r'''
            (?:`[^`\\]*(?:\\.[^`\\]*)*`)|  # single-quoted name
            (?: [a-zA-Z]+\w*)              # unquoted name
        ''', re.VERBOSE)

    def __init__(self, headers, ignore_case=False):
        """
        :param headers (Sequence or dict): can be a sequence of header names
            or a dictionary of index:name.

        """
        if not isinstance(headers, dict):
            headers = dict((j, i) for i, j in enumerate(headers))
        self.headers = self.orig_headers = headers
        self.ignore_case = ignore_case

    def lowercase_headers(self):
        return dict((k, v.lower()) for k, v in self.headers)

    def lowercase_name(self, name):
        return name[0].lower() if self.ignore_case else name[0]

    def validate_headers(self):
        # check for duplicate headers
        pass

    def names_to_indices(self, text):
        """uses back quotes to distinguish header names from regular quotes"""
        headers = (self.lowercase_headers() if self.ignore_case
                   else self.headers)
        headers = {i.replace(' ', '_'): j for i, j in headers.items()}
        tokens = self.__class__.column_names.scanString(text)
        result = ''
        last_stop = 0
        for token, start, stop in tokens:
            name = token[0].strip('`')
            header = name.lower() if self.ignore_case else name
            header = header.replace(' ', '_')
            if header not in headers:
                msg = 'Unknown column name {!r}.'.format(name)
                raise InvalidSliceString(dict(msg=msg, column=start))
            if start - last_stop > 0:
                result += text[last_stop:start]
            last_stop = stop
            result += str(headers[header])
        return result


headers = ['col 1', 'col 2', 'c', 'd', 'col 5']
text = '`col 2`:`col 5`:2, c, `col 1`'
print(headers)
print(text)
h = Headers(headers)
print(h.names_to_indices(text))
