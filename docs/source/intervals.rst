Masetering intervals
====================

The Interval class allows slicing, introspection and conversion of closed,
left-open, right-open and open intervals. It also supports conversion between
zero & unit-based endpoints, left & right bounded/unbounded endpoints,
abolute/relative indices, and stepped intervals. Most of the attributes &
properties as defined in `Intervals (mathematics)
<http://en.wikipedia.org/wiki/Interval_(mathematics))#Terminology>`_ are
available.



Interval Attributes
-------------------

===========  ===========================
origin       :code:`0` or :code:`1`
lower_bound  EndPoint()
upper_bound  EndPoint()
type         :code:`'closed'`, :code:`'left-open'`, :code:`'right-open'` or :code:`'open'`
===========  ===========================


Interval Types
--------------

==========  =============  ========================================
 Interval    Notation       Items Sliced from Sequence
==========  =============  ========================================
Closed      [start, stop]  Items from start to stop
Left-Open   (start, stop]  Items after start to stop
Right-Open  [start, stop)  Items from start to, but not incl. stop
Open        (start, stop)  Items after start to, but not incl. stop
==========  =============  ========================================


Interval Properties (boolean)
-----------------------------

+--------------+-----------------+--------------+----------------+
| * empty      | * bounded       | * closed     | * half-closed  |
| * proper     | * left_bounded  | * left-open  | * left-closed  |
| * degenerate | * right_bounded | * right-open | * right-closed |
| * reversed   | * unbounded     | * open       | * half-open    |
+--------------+-----------------+--------------+----------------+

<http://en.wikipedia.org/wiki/Interval_(mathematics))#Terminology>_

Interval Methods
----------------

+-----------------------------+----------------------------+
| * set                       | * to_closed_interval       |
| * to_slice                  | * to_left_open_interval    |
| * to_zero_based_endpoints   | * to_right_open_interval   |
| * to_unit_based_endpoints   | * to_open_interval         |
+-----------------------------+----------------------------+

Method Signatures
^^^^^^^^^^^^^^^^^
All returned `start`, `stop` values are integers and the `to_slice` method
returns a Python slice object ...

.. code-block:: python

    interval = Interval(start=None, stop=None, step=None,
                        type_='closed', origin=1)

    interval.set(self, start=None, stop=None, step=None)

    start, stop = interval.to_zero_based(start=False, stop=False)
    start, stop = interval.to_unit_based(start=False, stop=False)

    start, stop = to_open(start=False, stop=False, step=False,
                          from_type=False, to_origin=False):
    start, stop = to_left_open(start=False, stop=False, step=False,
                               from_type=False, to_origin=False)
    start, stop = to_right_open(start=False, stop=False, step=False,
                               from_type=False, to_origin=False)
    start, stop = to_open(start=False, stop=False, step=False,
                          from_type=False, to_origin=False)

    slice_ = interval.to_slice(start=None, stop=None, step=None)

.. Attention:: :code:`False is not None`
  Start & stop can be set to `False`, `None` or an `int`.  When set to False
  the arg will bet set to the value of the class instance property; otherwise,
  the arg will be hard-coded with the value provided.  Allowing any of the args
  to be hard-coded allows any instance of an Interval to be used a calculator
  for different origins & interval types.


Dependencies
------------

Requires EndPoint class for handling lower & upper bound.


Endpoints
=========

The EndPoint class is used for handling the interval's lower and upper bounds.
It supports zero and unit-based endpoints along with unbounded conditions.
It also ensures endpoint values remain sane when used with add and subtract
operators and provides relational operators for the endpoints.

Endpoint Attributes & Properties
--------------------------------

+------------+----------------------------+
| Attributes | EndPoint Properties (bool) |
+============+=============+==============+
| * origin   | * bounded   | * absolute   |
| * value    | * unbounded | * relative   |
+------------+-------------+--------------+

Dependencies
------------
None