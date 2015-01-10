# -*- coding: utf-8 -*-
from collections import Iterator, Sequence
from itertools import chain
chained = chain.from_iterable

from .grammar import Grammar
from .headers import Headers
from .interval import Interval

# convert to 2-d sequence
# slicing required? (empty or copy [:])
# headers_to_colnums

def _preprocess(seq, slicestr, headers, ignorecase):
    if not seq:
        return (_ for _ in ()), None
    if isinstance(slicestr, int):
        slicestr = str(slicestr)
    slicestr = slicestr.replace('None', '')
    first_item = None
    try:
        is_2d_list = isinstance(seq[0], Sequence)
    except TypeError:
        try:
            first_item = next(seq)
            seq = chain(first_item, seq)
        except TypeError:
            raise
        except StopIteration:
            return (_ for _ in ()), None
    if not isinstance(first_item, (Iterator, Sequence)):
        seq = list(seq)
    if not slicestr or slicestr.strip() == ':':
        return seq, None
    if headers:
        h = Headers(headers, ignorecase)
        slicestr = h.names_to_indices(slicestr)
    return seq, slicestr


def as_list(seq):
    return list(map(list, seq))


def slice_(seq, slicestr, dialect=None, headers=None, ignorecase=False,
           grammar=None):
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
    :raises:             InvalidSliceString

    >>> seq = [['a1', 'a2', 'a3'], ['b1', 'b2', 'b3']]
    >>> list(sliced(seq, '2:'))
    [['a2', 'a3'], ['b2', 'b3']]
    """
    seq, slicestr = _preprocess(seq, slicestr, headers, ignorecase)
    if slicestr is None:
        return seq
    if not grammar:
        grammar = Grammar(dialect)
    grammar.allow_slice_list = False
    slice_ = Interval(**grammar.parse(slicestr)).to_slice()
    return (i[slice_] for i in seq)


def slices(seq, slicestr, dialect=None, headers=None, ignorecase=False):
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

    >>> list(sliced(seq, '1..3', 'double_dot'))
    [['a1', 'a2', 'a3'], ['b1', 'b2', 'b3']]

    >>> list(sliced(seq, '1...3', 'double_dot'))
    [['a1', 'a2'], ['b1', 'b2']]
    """
    grammar = Grammar(dialect)
    if not grammar.allow_slice_list or grammar.list_sep not in slicestr:
        return slice_(seq, slicestr, dialect, headers, ignorecase, grammar)
    seq, slicestr = _preprocess(seq, slicestr, headers, ignorecase)
    if slicestr is None:
        return seq
    slices = [Interval(**i).to_slice() for i in grammar.parse(slicestr)]
    return (chained((i[j] for j in slices)) for i in seq)


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

if __name__ == '__main__':
    import doctest
    doctest.testmod()