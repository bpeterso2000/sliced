# -*- coding: utf-8 -*-
"""
Allows header names to be used in slice strings
===============================================
Translates column header names in slice strings to indices.  Configurable
support for single & double-quoted names, wildcards, regular expressions,
spreadsheet-style alpha ID column headers, column numbers, and hybrid
combinations of these types.  Leverages the Grammar class to supports provide
support for different slice string grammars & dialects.
"""

import re
import sys
from collections import Counter, Iterable, OrderedDict
from functools import partial

import pyparsing as pp
from pyparsing import Regex, ParseException

from .exceptions import InvalidSliceString
from .grammar import Grammar


def pipe(data, *funcs):
    """ Pipe a value through a sequence of functions
    I.e. ``pipe(data, f, g, h)`` is equivalent to ``h(g(f(data)))``
    We think of the value as progressing through a pipe of several
    transformations, much like pipes in UNIX
    ``$ cat data | f | g | h``
    >>> double = lambda i: 2 * i
    >>> pipe(3, double, str)
    '6'

    source: github.com/pytoolz
    """
    for func in funcs:
        data = func(data)
    return data


class Headers(object):
    """
    Class for parsing headers in slice strings & translating them to indexes 
    ------------------------------------------------------------------------
    * If both header names & alpha-ids are used, header names take precedence.
    * The header name must be enclosed in quotes if the header name:
        * Is numeric-only and both header_names & colnums are enabled.
        * Contains separator characters (sep chars are defined in dialect).
        * Contains literal ? or * characters and wildcards are enabled.
    * Header names can be single or double quoted.
    * Escape literal quote characters inside headers names with a backslash.
    """

    def __init__(self, headers=None, grammar=None, origin=1, ignorecase=True,
                 allow_alphaids=False, allow_colnums=True,
                 allow_wildcards=True, allow_regexes=True,
                 replace_whitespace=True, whitespace=r'\s+',
                 number_duplicates=True):

        self.headers = headers if headers else {}
        self.grammar = grammar if grammar else Grammar()
        self.origin = origin

        self.ignorecase = ignorecase
        self.number_duplicates = number_duplicates

        self.allow_alphaids = allow_alphaids
        self.allow_colnums = allow_colnums
        self.allow_wildcards = allow_wildcards
        self.allow_regexes = allow_regexes

        # --- HEADER MUNGING ---
        # keys can be toggled on/off by with a class attrib of the same name
        # values are the transformation functions
        # partial function keywords can only be set during class construction
        # or by explicitly updating the partial function in the translation 
        # attribute
        replace_whitespace = '_' if replace_whitespace else None
        self.translation = OrderedDict({
            'ignorecase':         ignorecase_,
            'replace_whitespace': partial(replace_whitespace_,
                                          whitespace=whitespace,
                                          replace_with=replace_whitespace),
            'number_duplicates':  number_duplicates_
        })

        # --- SLICE STRING HEADER PARSING ---
        # keys can be toggled on/off by with a class attrib of the same name
        # prefixed with allow_
        # except for keys starting with an underscore, they are always on
        seps = list({self.grammar.list_sep, self.grammar.range_sep,
                     self.grammar.step_sep})
        quotedstr = pp.quotedString.setParseAction(pp.removeQuotes)
        self.tokenizers = OrderedDict({
            'regexes': 'r' + quotedstr,
            '_quoted': quotedstr,
            'colnums': Grammar.integer,
            '_sep':    Or(seps),
            '_names':  CharsNotIn(seps),
        })

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, names):
        """
        :param names: list of header names or dict of column indexes: names
        :type names: [str, ...] or [(int, str), ...] or {int: str}, 
        """
        try:
            self._headers = dict(names)
        except ValueError as error:
            self._headers = dict(enumerate(names))

    # --- HEADER TRANSLATION FUNCTIONS ---

    @staticmethod
    def replace_whitespace_(headers, replace_with='_'):
        if replace_with:
            if not isinstance(replace_with, str):
                replace_with = '_'
            return {k: WHITESPACE.sub(replace_with, v)
                    for k, v in headers.items()}
        return headers

    @staticmethod
    def ignorecase_(headers):
        return {k: v.lower() for k, v in headers.items()}

    @staticmethod
    def number_duplicates_(headers, numfmt='{name}-{num}'):
        """
        Numbers duplicate header names to avoid ambiguity
        :param headers: dict of column indexes and associated header names
        :type headers:  {int, str}
        """
        hdrfmt = numsep.join(['{[1]}', '{}'])
        duplicates = {k: v for k, v in Counter(headers.values()).items() if v > 1}
        for duplicate in duplicates:
            dups = {k: v for k, v in headers.items() if v == duplicate}
            sorted_dups = enumerate(sorted(duplicated.items()), 1)
            headers.update ({i[0]: numfmt.format(name=i[0], num=n)
                            for n, i in sorted_dups})
        return headers

    # --- SPREADSHEET-STYLE COLUMN ALPHA ID HEADERS ---

    @staticmethod
    def id2num(s):
        """ spreadsheet column name to number
        http://stackoverflow.com/questions/7261936

       :param s: str -- spreadsheet column alpha ID (i.e. A, B, ... AA, AB,...)
       :returns: int -- spreadsheet column number (zero-based index)

        >>> id2num('A')
        0
        >>> id2num('B')
        1
        >>> id2num('XFD')
        16383
        >>>

        """
        n = 0
        for ch in s.upper():
            n = n * 26 + (ord(ch) - 65) + 1
        return n - 1


    @staticmethod
    def num2id(n):
        """
        reference: http://stackoverflow.com/questions/181596

       :param n: int -- spreadsheet column number (zero-based index)
       :returns: int -- spreadsheet column alpha ID (i.e. A, B, ... AA, AB,...)

        >>> num2id(0)
        'A'
        >>> num2id(1)
        'B'
        >>> num2id(16383)
        'XFD'

        """
        s = ''
        d = n + 1
        while d:
            m = (d - 1) % 26
            s = chr(65 + m) + s
            d = int((d - m) / 26)
        return s

    @staticmethod
    def get_ids(num_ids):
        return {i: num2id(i) for i in range(num_ids)}

    def add_alphaids(self):
        num_ids = 0
        if self.allow_alphaids:
            if not isinstance(self.allow_alphaids, [int, float]):
                num_ids = (len(pp.alphas) // 2) ** 2
            num_ids = int(self.allow_alphaids)
        return [num2id(i + 1) for i in range(num_ids)]

    def munge_headers(self):
        functs = [v for k, v in self.translation.items() if getattr(self, k)]
        return pipe(add_alphaids().update(self.headers), *functs)

    def parse_text(self, text):
        try:
            return self.tokenizer.parseString(text)
        except ParserException as error:
            info = {'text': text, 'column': error.column}
            raise InvalidSliceString(error.msg, info)

    def build_parser(self):
        tokenizers = [v.setResultsName(k) for k, v in self.tokenizers.items()
                      if not k.startswith('_') and getattr(self, k, True)]
        return ZeroOrMore(Group(Or(tokenizers))) + pp.stringEnd


"""
tokenizer = []
if self.allow_regexes:
    regex  = 'r' + pp.quotedString.setParseAction(pp.removeQuotes)
    tokenizer.append(regex.setResultsName('regex'))
quoted_name = pp.quotedString.setParseAction(pp.removeQuotes)
tokenizer.append(quoted_name.setResultsName('name'))
if self.allow_colnums:
    tokenizer.append(Grammar.integer.setResultsName('colnum'))
seps = list({self.grammar.list_sep, self.grammar.range_sep,
             self.grammar.step_sep})
tokenizer.append(Or(seps).setResultsName('sep'))
tokenizer.append(CharsNotIn(seps).setResultsName('name'))
self.tokenizer = ZeroOrMore(Group(Or(tokenizer))) + pp.stringEnd
"""