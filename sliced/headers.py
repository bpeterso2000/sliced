# -*- coding: utf-8 -*-
"""
Allows header names to be used in slice strings
===============================================
Converts header names to indices.
"""

import re
from collections import Counter

from pyparsing import Regex

from .exceptions import InvalidSliceString, DuplicateItemsNotAllowed


class Headers(object):

    column_names = Regex(r'''
            (?:`[^`\\]*(?:\\.[^`\\]*)*`)|  # single-quoted name
            (?: [a-zA-Z]+\w*)              # unquoted name
        ''', re.VERBOSE)

    def __init__(self, headers, ignorecase=False):
        """
        :param headers (Sequence or dict): can be a sequence of header names
            or a dictionary of index:name.
        """
        self.headers = headers
        self.ignorecase = ignorecase

    @property
    def headers(self):
        return getattr(self, '_headers', {})

    @headers.setter
    def headers(self, headers):
        if not isinstance(headers, dict):
            header_test = header_dict = {j: i for i, j in enumerate(headers)}
            if self.ignorecase:
                header_test = self.lowercase_keys(header_dict)
            self.validate_headers(headers, header_test)
            self._headers = header_dict

    @property
    def ignorecase(self):
        return getattr(self, '_ignorecase', False)

    @ignorecase.setter
    def ignorecase(self, enabled):
        if enabled:
            lowercase_headers = self.lowercase_keys(self.headers)
            self.validate_headers(self.headers, lowercase_headers)
        self._ignorecase = enabled

    @staticmethod
    def lowercase_keys(dict_):
        return {k.lower(): v for k, v in dict_}

    def lowercase_name(self, name):
        return name[0].lower() if self.ignorecase else name[0]

    def validate_headers(self, headers, new_dict):
        if len(headers) != len(new_dict):
            dups = [k for k, v in Counter(new_dict).items() if v]
            mesg = 'Duplicate headers.'
            raise DuplicateItemsNotAllowed({'mesg': mesg, 'dups': dups})

    def names_to_indices(self, text):
        """uses back quotes to distinguish header names from regular quotes"""
        headers = (self.lowercase_keys(self.headers) if self.ignorecase
                   else self.headers)
        headers = {i.replace(' ', '_'): j for i, j in headers.items()}
        tokens = self.__class__.column_names.scanString(text)
        result = ''
        last_stop = 0
        for token, start, stop in tokens:
            name = token[0].strip('`')
            header = name.lower() if self.ignorecase else name
            header = header.replace(' ', '_')
            if header not in headers:
                mesg = 'Unknown column name {!r}.'.format(name)
                raise InvalidSliceString(mesg, {'column': start})
            if start - last_stop > 0:
                result += text[last_stop:start]
            last_stop = stop
            result += str(headers[header])
        result = text[last_stop:]
        return result
