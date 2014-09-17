How-to slice
============

.. sidebar:: Visualizing 2-d Sequences

    A 2-d sequence can be though of as a spreadsheet, where the outer sequence
    is rows, the inner sequence is columns and the objects are cells.

Sliced comes packaged with three (3) high-level helper functions used to slice
objects from a sequence of sequences. These helpers are wrappers around the
Grammar & Interval classes and each returns a generator to effeciently produce
a list of sliced columns for each row.


Helper functions
----------------

============  ===============================================================
**`slices`**  slice a sequence using specified dialect (supports slice lists)
**`slice_`**  same as slices (faster, but doesn't support slice lists)
**`cut`**     same a slices, but dialect is hard-coded to 'unix_cut'
============  ===============================================================

Examples::

    sliced_row_gen = slices(rows, '1, 3, 4:8, -1')
    sliced_row_gen = slices(rows, '1..10, 14::2', 'dot_notation')
    sliced_row_gen = slice_(rows, ':8')
    sliced_row_gen = slice_(rows, '2-4, 7', 'unix-cut')
    sliced_row_gen = cut(rows, '2-4, 7')
    sliced_rows = list(cut(rows, '2-4, 7'))

Parameters:
===========  ==========  ===================================================
sequence     (Sequence)  a 2-d sequence containing the objects to be sliced
slicestring  (str)       a slice string in the specified dialect
dialect      (str)       a dialect name defined in Grammar
===========  ==========  ===================================================

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


slices
^^^^^^

.. code-block:: python

    In [1]: from pprint import pprint

    In [2]: from sliced import slices

    In [3]: sequence = [
       ...:     ['alpha-1', 'alpha-2', 'alpha-3', 'alpha-4', 'alpha-5', 'alpha-6'],
       ...:     ['beta-1', 'beta-2', 'beta-3', 'beta-4', 'beta-5', 'beta-6'],
       ...:     ['gamma-1', 'gamma-2', 'gamma-3', 'gamma-4', 'gamma-5', 'gamma-6']
       ...: ]

    In [4]: slicestring = '2:4, -1'

    In [5]: dialect = 'python_slice'

    In [6]:

    In [6]: new_slices = slices(sequence, slicestring, dialect)

    In [7]: type(new_slices)
    Out[7]: generator

    In [8]: pprint(list(new_slices))
    [['alpha-2', 'alpha-3', 'alpha-4', 'alpha-6'],
     ['beta-2', 'beta-3', 'beta-4', 'beta-6'],
     ['gamma-2', 'gamma-3', 'gamma-4', 'gamma-6']]

In the above example we used the 'python_slice' format.  This is the default
format: dialect='python_slice', dialect=None or not including dialect as a
parameter will all have the same effect.  The `python_slice` dialect behaves
just like a standard Python slice syntax except that:

- Indices are unit-based (origin=1) instead of zero-based.
- Slices are closed-intervals instead of a right-open.
- Supports slice lists (comma separated)

slice_()
--------
Same as `slices()` except that it only handles a single slice.  Even if the
selected dialect supports slice lists, the grammar will be rebuilt to disallow
the slice list syntax.  The advantage of this function over `slices()` is that
it is lightweight and faster since there is only one sliced list, it doesn't
need to chain the resulting sliced lists back together.

.. code-block:: python

    new_slice = slice_(sequence, slicestring, dialect)

cut()
-----
Shortcut for code: slices(sequence, slicestring, dialect='unix-cut')

.. code-block:: python

    new_slice = cut(sequence, slicestring)
