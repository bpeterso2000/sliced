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
