# -*- coding: utf-8 -*-
from itertools import chain
chained = chain.from_iterable

from .grammar import Grammar
from .interval import Interval


def get_slice(seq, text, dialect=None):
    """
    extract columns from rows using a single slice
    ----------------------------------------------
    Similar to the sliced function, but faster; slice lists are not allowed.
    :param seq: (Sequence) - A 2-d Sequence to slice (i.e. rows & columns)
    :param text: (str) - Slice string specified in the selected dialect.
    :param dialect: (str) - Slice string dialect name; used to build grammar.
                            The dialect must be None (default) or a dialect
                            as described in the Grammar class.
    :returns: (generator) - produces a list of sliced objects for each 
                            each item in the sequence.

    >>> seq = [['a1', 'a2', 'a3'], ['b1', 'b2', 'b3']]
    >>> list(sliced(seq, '2:'))
    [['a2', 'a3'], ['b2', 'b3']]
    """
    grammar = Grammar(dialect)
    grammar.allow_slice_list = False
    slice_ = Interval(**grammar.parse(text)).to_slice()
    return (i[slice_] for i in seq)


def sliced(seq, text, dialect=None):
    """
    extract columns from rows using one or more slice strings
    ---------------------------------------------------------
    :param seq: (Sequence) - A 2-d Sequence to slice (i.e. rows & columns)
    :param text: (str) - Slice string specified in the selected dialect.
    :param dialect: (str) - Slice string dialect name; used to build grammar.
                            The dialect must be None (default) or a dialect
                            as described in the Grammar class.
    :returns: (generator) - produces a list of sliced objects for each 
                            each item in the sequence.

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
    slices = [Interval(**i).to_slice() for i in Grammar(dialect).parse(text)]
    return (list(chained((i[j] for j in slices))) for i in seq)


def cut(seq, text):
    """
    extract columns from rows using Unix cut-style syntax
    -----------------------------------------------------
    :param seq: (Sequence) - A 2-d Sequence to slice (i.e. rows & columns)
    :param text: (str) - Slice string specified in Unix-cut syntax
    :returns: (generator) - produces a list of sliced objects for each 
                            each item in the sequence.

    >>> seq = [['a1', 'a2', 'a3'], ['b1', 'b2', 'b3']]
    >>> list(cut(seq, '2-, 1'))
    [['a2', 'a3', 'a1'], ['b2', 'b3', 'b1']]
    """
    return sliced(seq, text, 'unix_cut')
