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
from collections import OrderedDict

import pyparsing as pp
from pyparsing import (CharsNotIn, Group, Literal, Or, Regex, ParseException,
    ZeroOrMore)
from toolz import curry, merge, pipe, valmap
from unidecode import unidecode

from .alphaids import id2num, num2id, get_ids, add_alphaids
from .slugs import Slugs, slugify
from ..exceptions import InvalidSliceString
from ..grammar import Grammar

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
    * headers format name: idx
    """

    def __init__(self, headers=None, slugify=None, origin=1, grammar=None, 
                 allow_alphaids=False, allow_colnums=True,
                 allow_wildcards=True, allow_regexes=True):
        self.origin = origin
        self.slugify = slugify if slugify else slugs.slugify
        self.ignorecase = ignorecase
        self.allow_alphaid = allow_alphaids
        self.allow_colnum = allow_colnums
        self.allow_wildcard = allow_wildcards
        self.allow_regex = allow_regexes
        self.grammar = grammar if grammar else Grammar()
        self.headers = headers

    @property
    def headers(self):
        return self._headers

    @headers.setter
    def headers(self, items):
        """
        :param names: list of header names or dict of column indexes: names
        :type names: [str, ...] or [(int, str), ...] or {int: str}, 
        """
        if items:
            if isinstance(items[0], str):
                numbered_items = enumerate(items, self.origin)
                items = OrderedDict((j, i) for i, j in numbered_items)
            slugs_ = self.slugify(self.headers.keys())
            self._headers = dict(zip(slugs_, self.headers.values))
        elif self.allow_alphaids:
            self.headers = add_alphaids()

    @property
    def grammar(self):
        return self._grammar

    @grammar.setter
    def grammar(self, value):
        seps = list({
            value.list_sep,
            value.range_sep,
            value.step_sep
        })
        quotedstr = pp.quotedString.setParseAction(pp.removeQuotes)

        self.tokens = OrderedDict({
            'regex': Literal('r').suppress() + quotedstr,
            'quoted': quotedstr,
            'colnum': Grammar.integer,
            'sep': Or(seps),
            'name': CharsNotIn(seps),
        })

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
