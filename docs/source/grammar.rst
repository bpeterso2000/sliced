Learning dialects & grammars
============================

The Grammar class allows different dialects to be used to enter slice
information. It is able to provide location information for syntax errors and
allows the creation of custom grammars through the following attributes:

=======================  ==========
Grammar attribute        data type
=======================  ==========
range_sep                re pattern
step_sep                 str
list sep                 str
allow_relative_indices   bool
allow_stepped_intervals  bool
allow_reversed_stride    bool
allow_slice_list         bool
interval                 dict
=======================  ==========

Interval is a mapping of matched range-sep to interval-type

Methods
^^^^^^^

.. code-block:: python

    grammar = Grammar(dialect=None)
    is_valid = grammar.validate_separators()
    set_interval_args_dict = parse_text(self, single_slice_string)
    set_interval_args_dict = parse(self, string_containing_a_slice)
    interval_args_generator = parse(self, string_of_zero_or_more_slices)


Built-in dialects
^^^^^^^^^^^^^^^^^

=================
Built-in dialects
=================
* slice_list (default)
* python_slice
* unix_cut
* dot_notation
* ruby_range
=================


Exception Handling
------------------

InvalidSliceString
^^^^^^^^^^^^^^^^^^
Generated when the text does not match the grammar.

EndPointValueError
^^^^^^^^^^^^^^^^^^
Generated when zero is not a valid index, i.e. unit-based slices.


Python Slice (default)
----------------------

=========  =====
Separator  Value
=========  =====
range_sep  ``:``
step_sep   ``:``
list_sep   ``,``
=========  =====

======================  =====
Attribute               Value
======================  =====
allow_relative_indices  True
allow_stepped_intervals True
allow_reversed_stride   True
allow_slice_list        True
======================  =====

=========  =============
range_sep  interval type
=========  =============
``:``      closed
=========  =============


UNIX Cut
--------

=========  =====
Separator  Value
=========  =====
range_sep  ``:``
list_sep   ``,``
=========  =====

======================  =====
Attribute               Value
======================  =====
allow_relative_indices  False
allow_stepped_intervals False
allow_reversed_stride   False
allow_slice_list        True
======================  =====

=========  =============
range_sep  interval type
=========  =============
``-``      closed
=========  =============


Dot Notation
------------

=========  ===============================================
Separator  Value
=========  ===============================================
range_sep  Optional('``.``') + '``:``' + Optional('``.``')
step_sep   ``:``
list_sep   ``,``
=========  ===============================================

======================  =====
Attribute               Value
======================  =====
allow_relative_indices  True
allow_stepped_intervals True
allow_reversed_stride   True
allow_slice_list        True
======================  =====

=========  =============
range_sep  interval type
=========  =============
``:``      closed
``.:``     left-open
``:.``     right-open
``..``     open
``.:.``    open
=========  =============

Ruby Range
----------
`Range <http://www.ruby-doc.org/core-2.1.2/Range.html>`_ as described in the
official Ruby docs.

=========  ==========================
Separator  Value
=========  ==========================
range_sep  ``..`` + Optional('``.``')
list_sep   ``,``
=========  ==========================

======================  =====
Attribute               Value
======================  =====
allow_relative_indices  True
allow_stepped_intervals False
allow_reversed_stride   False
allow_slice_list        True
======================  =====

=========  =============
range_sep  interval type
=========  =============
``..``     closed
``...``    right-open
=========  =============

Custom Dialects
---------------

You can extend the Grammar class to include your own dialects.  Just add a
method named '_dialect__' + <your dialect name>.  To inherit other dialects
just call the method.

The interval attribute is a dictionary used to create a lookup table to
determine the interval type based on the range separator.  The key is the range
separator and the value is any valid Interval class type ('closed',
'left-open', 'right-open', 'open').

If you want to test your new dialect you can just call the parse method.

.. code-block:: python

    grammar = Grammar(dialect=your-new-dialect)
    grammar.parse(text)
