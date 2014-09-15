Sliced
======

A Python slicing toolkit.


Project Resources
-----------------
* Read the Docs: http://sliced.rtfd.org
* Github: https://github.com/bpeterso2000/sliced
* Free software: Apache 2.0


Current tools provide support for:

- Slicing, introspection and conversion of closed, left-open, right-open
  and open intervals. It also supports conversion between zero & unit-based
  endpoints, left & right bounded/unbounded endpoints, abolute/relative
  indices, and stepped intervals. Most of the attributes & properties as
  defined in `Intervals (mathematics)
  <http://en.wikipedia.org/wiki/Interval_(mathematics))#Terminology>`_
  are provided.

- Different dialects to slice sequences, most of the dialects included support
  slice lists.  The grammar is dymacially assembled based on the chosen
  dialect, and can provide friendly feedback to point out the location of
  errors detected during text parsing.  Also provides support for creating
  your own custom slicing dialects.
