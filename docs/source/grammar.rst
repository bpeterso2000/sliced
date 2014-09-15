Grammar
=======

The Grammar class allows different dialects to be used to enter slice
information. It is able to provide location information for syntax errors and
allows creatiion of custom grammars.

.. code-block:: python

    grammar = Grammar(dialect=None)

Built in grammar dialects include:

+----------------+
| * Python Slice |
| * Unix Cut     |
| * Dot Notation |
| * Ruby Range   |
+----------------+


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

Separators
^^^^^^^^^^

+------------+-------+
| Attribute  | Regex |
+============+=======+
| range_sep  | ``:`` |
+------------+-------+
| step_sep   | ``:`` |
+------------+-------+
| list_sep   | ``,`` |
+------------+-------+

Features
^^^^^^^^

+-------------------------+-------+
| Attribute               | State |
+=========================+=======+
| allow_relative_indices  | True  |
+-------------------------+-------+
| allow_stepped_intervals | True  |
+-------------------------+-------+
| allow_reversed_stride   | True  |
+-------------------------+-------+
| allow_slice_list        | True  |
+-------------------------+-------+

Supported Intervals
^^^^^^^^^^^^^^^^^^^

+-----------+--------+
| range_sep | type   |
+===========+========+
| ``:``     | closed |
+-----------+--------+


UNIX Cut
--------

Separators
^^^^^^^^^^

+------------+-------+
| Attribute  | Regex |
+============+=======+
| range_sep  | ``-`` |
+------------+-------+
| list_sep   | ``,`` |
+------------+-------+

Features
^^^^^^^^

+-------------------------+-------+
| Attribute               | State |
+=========================+=======+
| allow_relative_indices  | False |
+-------------------------+-------+
| allow_stepped_intervals | False |
+-------------------------+-------+
| allow_reversed_stride   | False |
+-------------------------+-------+
| allow_slice_list        | True  |
+-------------------------+-------+

Supported Intervals
^^^^^^^^^^^^^^^^^^^

+-----------+--------+
| range_sep | type   |
+===========+========+
| ``-``     | closed |
+-----------+--------+


Dot Notation
------------

Separators
^^^^^^^^^^

+------------+------------------------+
| Attribute  | Regex                  |
+============+========================+
| range_sep  | ``(\.?:\.?)|(\.{2})``  |
+------------+------------------------+
| step_sep   | ``:``                  |
+------------+------------------------+
| list_sep   | ``,``                  |
+------------+------------------------+
Features
^^^^^^^^

+-------------------------+-------+
| Attribute               | State |
+=========================+=======+
| allow_relative_indices  | True  |
+-------------------------+-------+
| allow_stepped_intervals | True  |
+-------------------------+-------+
| allow_reversed_stride   | True  |
+-------------------------+-------+
| allow_slice_list        | True  |
+-------------------------+-------+

Supported Intervals
^^^^^^^^^^^^^^^^^^^

+-----------+------------+
| range_sep | type       |
+===========+============+
| ``:``     | closed     |
+-----------+------------+
| ``.:``    | left-open  |
+-----------+------------+
| ``:.``    | right-open |
+-----------+------------+
| ``.:.``   | open       |
+-----------+------------+
| ``..``    | open       |
+-----------+------------+


Ruby Range
----------
`Range <http://www.ruby-doc.org/core-2.1.2/Range.html>`_ as described in the
official Ruby docs.

Separators
^^^^^^^^^^

+------------+-------------+
| Attribute  | Regex       |
+============+=============+
| range_sep  | ``\.{2,3}`` |
+------------+-------------+
| list_sep   | ``,``       |
+------------+-------------+

Features
^^^^^^^^

+-------------------------+-------+
| Attribute               | State |
+=========================+=======+
| allow_relative_indices  | True  |
+-------------------------+-------+
| allow_stepped_intervals | False |
+-------------------------+-------+
| allow_reversed_stride   | False |
+-------------------------+-------+
| allow_slice_list        | True  |
+-------------------------+-------+

Supported Intervals
^^^^^^^^^^^^^^^^^^^

+-----------+------------+
| range_sep | type       |
+===========+============+
| ``..``    | closed     |
+-----------+------------+
| ``...``   | right-open |
+-----------+------------+


Custom Dialects
---------------

You can extend the Grammar class to include your own dialects.  Just add a
method named '_dialect__' + <your dialect name>.  To inherit other dialects
just call the method.

The interval attribute is a dictory used to create a lookup table to determine
the interval type based on the range separator.  The key is the range separator
and the value is any valid Interval class type ('closed', 'left-open',
'right-open', 'open').

If you want to test your new dialect you can just call the parse method.

.. code-block:: python

    grammar = Grammar(dialect=your-new-dialect)
    grammar.parse(text)

.. toctree::
   :maxdepth: 2
   :hidden:
