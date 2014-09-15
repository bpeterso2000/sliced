Intervals
=========

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
| * proper     | * left_bounded  | * left_open  | * left_closed  |
| * degenerate | * right_bounded | * right_open | * right_closed |
| * reversed   | * unbounded     | * open       | * half-open    |
+--------------+-----------------+--------------+----------------+


Interval Methods
----------------

+-----------------------------+----------------------------+
| * set                       | * to_closed_interval       |
| * to_slice                  | * to_left_open_interval    |
| * to_zero_based_endpoints   | * to_right_open_interval   |
| * to_unit_based_endpoints   | * to_open_interval         |
+-----------------------------+----------------------------+


Dependencies
------------

Requires EndPoint class for handling lower & upper bound.

.. toctree::
   :maxdepth: 2
   :hidden:
