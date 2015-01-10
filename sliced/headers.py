# -*- coding: utf-8 -*-
"""
Allows header names to be used in slice strings
===============================================
Translates column header names in slice strings to indices.  Configurable
support for single & double-quoted names, wildcards, regular expressions,
spreadsheet-style alpha ID column headers, column numbers, and hybrid
combinations of these types.  Leverages the Grammar class to supports provide
support for different slice string grammars & dialects.

headers is a dictionary { column-index: name, ...}
where column index is zero-based if origin is 0 or unit-based if origin is 1

"""

import re
import sys
from collections import Counter, OrderedDict

import pyparsing as pp
from pyparsing import CharsNotIn, Group, Or, Regex, ParseException, ZeroOrMore
from toolz import curry, merge, pipe, valmap
from unidecode import unidecode

from .exceptions import InvalidSliceString
from .grammar import Grammar


def compile_regex(pattern):
    return re.compile(pattern) if isinstance(pattern, str) else pattern


def is_str(s):
    return isinstance(str, s)


def to_dict(obj):
    try:
        return dict(names)
    except ValueError:
        return dict(enumerate(names))


def items(obj):
    return to_dict(obj).items()


# --- HEADER TRANSLATIONS (MUNGING) ---

def lowercase(headers):
    return valmap(str.lower, headers)


def remove_accent(headers):
    return valmap(unidecode)


@curry
def sub(headers, repl='', regex=r''):
    whitespace = compile_regex(whitespace)
    return {k: whitespace.sub(repl, v) for k, v in items(headers)}


@curry
def slug(headers, deaccent=True, ignorecase=True,
         whitespace='_', nonalphanum='',
         whitespace_re=r'\s+', nonalphanum_re=r'[^\w_]'):
    actions = (
        (remove_accent, deaccent),
        (lowercase, ignorecase),
        (sub(whitespace, whitespace_re), is_str(whitespace)),
        (sub(nonalphanum, nonalphanum_re), is_str(nonalphanum))
    )
    pipe(headers, *(funct for funct, enabled in actions if enabled))


@curry
def enum_dups(headers, numfmt='{name}-{num}'):
    """
    Numbers duplicate header names to avoid ambiguity
    :param headers: dict of column indexes and associated header names
    :type headers:  {int, str}

    >>> number_duplicates_({0:'date', 1:'value', 2:'date'})
    {0: 'date-1', 1: 'value', 2: 'date-2'}

    """
    hdrs = dict_(headers)
    format_name = lambda name, num: numfmt.format(name=name, num=num)
    duplicates = {k: v for k, v in Counter(hdrs.values()).items() if v > 1}
    for duplicate in duplicates:
        dups = {k: v for k, v in hdrs.items() if v == duplicate}
        sorted_dups = enumerate(sorted(dups.items()), 1)
        headers.update ({i[0]: format_name(n, i) for n, i in sorted_dups})
    return headers

# --- SPREADSHEET-STYLE COLUMN ALPHA ID HEADERS ---

def id2num(s):
    """ spreadsheet column name to number
    ref: http://stackoverflow.com/questions/7261936

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


def num2id(n):
    """
    ref: http://stackoverflow.com/questions/181596

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


def get_ids(num_ids):
    return {i: num2id(i) for i in range(num_ids)}


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

    def __init__(self, headers=None,
                 grammar=None, origin=1,
                 deaccent=True, ignorecase=True,
                 allow_alphaids=False, allow_colnums=True,
                 allow_wildcards=True, allow_regexes=True,
                 whitespace='_', nonalphanums='',
                 numfmt='{name}-{num}'):

        self.origin = origin
        self.headers = headers if headers else {}
        self.grammar = grammar if grammar else Grammar()

        self.ignorecase = ignorecase
        self.allow_alphaid = allow_alphaids
        self.allow_colnum = allow_colnums
        self.allow_wildcard = allow_wildcards
        self.allow_regex = allow_regexes

        # --- HEADER MUNGING FUNCTIONS ---
        self.munge = OrderedDict([
            ('slugify', slug(deaccent=deaccent,
                             ignorecase=ignorecase,
                             whitespace=whitespace,
                             nonalphanums=nonalphanums)),
            ('number_duplicates', enum_dups(numfmt=numfmt))
        ])

        # --- HEADER PARSING FUNCTIONS ---
        seps = list({
            self.grammar.list_sep,
            self.grammar.range_sep,
            self.grammar.step_sep
        })
        quotedstr = pp.quotedString.setParseAction(pp.removeQuotes)

        self.tokens = OrderedDict({
            'regex': 'r'.Supress() + quotedstr,
            'quoted': quotedstr,
            'colnum': Grammar.integer,
            'sep': Or(seps),
            'name': CharsNotIn(seps),
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

    def add_alphaids(self):
        num_ids = 0
        if self.allow_alphaids:
            try:
                num_ids = int(self.allow_alphaids)
            except (TypeError, ValueError):
                num_ids = 676
        return {i: num2id(i + 1) for i in range(num_ids)}

    def munge_headers(self):
        functs = (v for k, v in self.munge.items()
                  if getattr(self, 'allow_' + k, True))
        return pipe(merge(self.add_alphaids(), self.headers), *functs)

    def parse_text(self, text):
        try:
            return self.tokenizer.parseString(text)
        except ParserException as error:
            info = {'text': text, 'column': error.column}
            raise InvalidSliceString(error.msg, info)

    def build_parser(self):
        tokens = (v.setResultsName(k) for k, v in self.tokens.items()
                  if not k.startswith('_') and getattr(self, k, True))
        return ZeroOrMore(Group(Or(tokens))) + pp.stringEnd
