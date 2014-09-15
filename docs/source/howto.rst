How-To
======

See :doc::`examples`_.

.. Note::

    This page is under construction

Core functions:

.. code-block:: python

    get_slice(sequence, slicestring, dialect)
    sliced(sequence, slicestring, dialect)
    cut(sequence, slicestring)

>>> list(sliced(seq, '1.:.3', 'dot_notation'))
[['a2'], ['b2']]

>>> list(sliced(seq, '1.:3', 'dot_notation'))
[['a2', 'a3'], ['b2', 'b3']]

>>> list(sliced(seq, '1..3', 'ruby_range'))
[['a1', 'a2', 'a3'], ['b1', 'b2', 'b3']]

>>> list(sliced(seq, '1...3', 'ruby_range'))
[['a1', 'a2'], ['b1', 'b2']]

.. code-block:: python

    >> interval.to_slice(-2, -1)
    slice(-2, -1, None)

.. toctree::
   :maxdepth: 2
   :hidden:
