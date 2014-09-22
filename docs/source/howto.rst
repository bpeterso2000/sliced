How-to use sliced
=================

Sliced comes packaged with three (3) high-level helper functions used to slice
objects from a sequence of sequences. These helpers are wrappers around the
Grammar & Interval classes.  Each returns a generator to effeciently produce
a list of sliced columns per each row.


Helper functions
----------------

:py:func:`slices`  slices a sequence using a specified dialect

:py:func:`slice_`  faster than slices whenever slice list support is not needed

:py:func:`cut`     same a slices, but the dialect is hard-coded to 'unix_cut'

Examples::

    from sliced import slices, slice_, cut

    sliced_row_gen = slices(rows, '1, 3, 4:8, -1')
    sliced_row_gen = slices(rows, '1..3, 5::2', 'dot_notation')
    sliced_row_gen = slice_(rows, ':5')
    sliced_row_gen = slice_(rows, '2-4, 7', 'unix-cut')
    sliced_row_gen = cut(rows, '2-4, 7')
    sliced_rows = list(cut(rows, '2-4, 7'))

.. py:function:: slices(seq, text, dialect=None)

    extract columns from rows using one or more slice strings
     
    :param Sequence seq: A 2-d Sequence to slice (i.e. rows & columns)
    :param str text:     Slice string specified in the selected dialect.
    :param str dialect:  Dialect name; used to build grammar and parse text.
                         The name must be defined in the Grammar class.
    :type dialect:       None or str
    :returns:            Produces a list of sliced objects per `seq` item.
    :rtype: generator

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


.. py:function:: slice_(seq, text, dialect=None)

    extract columns from rows using a single slice

    Similar to the sliced function, but faster; slice lists are not allowed.

    :param Sequence seq: A 2-d Sequence to slice (i.e. rows & columns)
    :param str text:     Slice string specified in the selected dialect.
    :param str dialect:  Dialect name; used to build grammar and parse text.
                         The name must be defined in the Grammar class.
    :type dialect:       None or str
    :returns:            Produces a list of sliced objects per `seq` item.
    :rtype: generator

    >>> seq = [['a1', 'a2', 'a3'], ['b1', 'b2', 'b3']]
    >>> list(sliced(seq, '2:'))
    [['a2', 'a3'], ['b2', 'b3']]


.. py:function:: cut(seq, text)

    extract columns from rows using Unix cut-style syntax

    :param Sequence seq: 2-d Sequence to slice (i.e. rows & columns)
    :param str text:     Slice string specified in the selected dialect.
    :returns:            Produces a list of sliced objects per `seq` item.
    :rtype:              generator

    >>> seq = [['a1', 'a2', 'a3'], ['b1', 'b2', 'b3']]
    >>> list(cut(seq, '2-, 1'))
    [['a2', 'a3', 'a1'], ['b2', 'b3', 'b1']]


Intervals
---------

Examples::

    interval = Interval()
    interval = Interval(start=2, type_='open')
    interval = Interval(start=None, stop=None, step=None, type_='closed', origin=1)
    slice_ = interval.to_slice()

Where `origin` is `0` or `1` and `type_` is one of the following:
- `closed`
- `left-open`
- `right-open`
- `open`

.. see also::

    Additional features in `Slicing with intervals`_


Grammar
-------

Dialects are described in further detail in the Grammar_ section.  Dialects
can have custom range separators, step-size separators and list separators.
In the case of `python_slice` the range-sep=':', step-sep=':' and list-sep=','
Range separators don't have to be just characters, they can be regular
expressions. Each dialect includes a dictionary that maps the range separator
matched during parsing to an interval type: closed, left-open, right-open or
closed. 

Examples::

    grammar = Grammar()
    grammar.allow_relative_indices = False
    grammar.allow_stepped_intervals = False
    grammar.allow_reversed_intervals = False
    grammar.allow_slice_lists = False

    grammar = Grammar('python_slice')
    interval_args_dict = grammar.parse_text('2:14:2')
    interval = Interval(**interval_args_dict)

    grammar = Grammar('dot_notation')
    interval_args = grammar.parse('5.:10:2, -4')
    intervals = (Interval(**i) for i in interval_args)

.. see also::

    Additional features in `Slicing with dialects & grammars`_

Parsing exceptions
^^^^^^^^^^^^^^^^^^

.. note::

    under construction

