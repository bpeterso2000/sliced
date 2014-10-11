# -*- coding: utf-8 -*-
from itertools import chain
chained = chain.from_iterable

from .grammar import Grammar
from .headers import Headers
from .interval import Interval


def slice_(seq, text, dialect=None, headers=None, ignorecase=False):
    """
    extract columns from rows using a single slice
    ----------------------------------------------
    Similar to the sliced function, but faster; slice lists are not allowed.

    :param Sequence seq: 2-d Sequence to slice (i.e. rows & columns)
    :param str text:     Slice string specified in the selected dialect.
    :param dialect:      Slice string dialect name; used to build grammar. The
                         dialect must be None or a dialect defined in the
                         Grammar class.
    :type dialect:       str or None
    :param headers:      header names and optional index positions
    :type headers:       list of strings or dictionary of indices (key=int)
                         and header name (value=str)
    :param ignorecase:   Indicates whether header names are case sensitive
    :type ignorecase:    bool
    :returns:            A list of sliced objects for each each item in the
                         sequence.
    :rtype:              generator

    >>> seq = [['a1', 'a2', 'a3'], ['b1', 'b2', 'b3']]
    >>> list(sliced(seq, '2:'))
    [['a2', 'a3'], ['b2', 'b3']]
    """
    if headers:
        h = Headers(headers, ignorecase)
        text = h.names_to_indices(text)
    grammar = Grammar(dialect)
    grammar.allow_slice_list = False
    slice_ = Interval(**grammar.parse(text)).to_slice()
    return (i[slice_] for i in seq)


def slices(seq, text, dialect=None, headers=None, ignorecase=False):
    """
    extract columns from rows using one or more slice strings
    ---------------------------------------------------------
    :param Sequence seq: 2-d Sequence to slice (i.e. rows & columns)
    :param str text:     Slice string specified in the selected dialect.
    :param str dialect:  Dialect name; used to build grammar and parse text.
                         The name must be defined in the Grammar class.
    :type dialect:       None or str
    :param headers:      header names and optional index positions
    :type headers:       list of strings or dictionary of indices (key=int)
                         and header name (value=str)
    :param ignorecase:   Indicates whether header names are case sensitive
    :type ignorecase:    bool
    :returns:            Produces a list of sliced objects per item in the seq.
    :rtype:              generator

    >>> seq = [['a1', 'a2', 'a3'], ['b1', 'b2', 'b3']]
    >>> list(sliced(seq, '2:, 1'))
    [['a2', 'a3', 'a1'], ['b2', 'b3', 'b1']]

    >>> list(sliced(seq, '1.:.3', 'dot_notation'))
    [['a2'], ['b2']]

    >>> list(sliced(seq, '1.:3', 'dot_notation'))
    [['a2', 'a3'], ['b2', 'b3']]

    >>> list(sliced(seq, '1..3', 'ruby_range'))
    [['a1', 'a2', 'a3'], ['b1', 'b2', 'b3']]

    >>> list(sliced(seq, '1...3', 'ruby_range'))
    [['a1', 'a2'], ['b1', 'b2']]
    """
    if headers:
        h = Header(headers, ignorecase)
        text = h.names_to_indices(text)
    slices = [Interval(**i).to_slice() for i in Grammar(dialect).parse(text)]
    return (list(chained((i[j] for j in slices))) for i in seq)


def cut(seq, text):
    """
    extract columns from rows using Unix cut-style syntax
    -----------------------------------------------------
    :param Sequence seq: 2-d Sequence to slice (i.e. rows & columns)
    :param str text:     Slice string specified in the selected dialect.
    :returns:            Produces a list of sliced objects per item in the seq.
    :rtype:              generator

    >>> seq = [['a1', 'a2', 'a3'], ['b1', 'b2', 'b3']]
    >>> list(cut(seq, '2-, 1'))
    [['a2', 'a3', 'a1'], ['b2', 'b3', 'b1']]
    """
    return slices(seq, text, 'unix_cut')
