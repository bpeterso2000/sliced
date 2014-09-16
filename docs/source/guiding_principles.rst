Guiding Principles
==================

Ensure portability
------------------
All tools in the kit are to be designed to be portable, i.e. pure-Python
without any requirement for compilers or pre-compiled binaries.


Minimize dependencies
---------------------
Dependencies are to be avoided, unless there are strong, compelling reasons to
include an external package.  The justification for including the package is
to be documented in the following paragraphs:

Currently the only dependency is pyparsing; this was chosen to allow other
developers to quickly and easily customize the grammar without getting bogged
down in the details.  It also provides detailed exception handling to help
users pinpoint the location of their invalid slicing syntax.

Easy to use
-----------
The tools are to be designed so that they are easy to use and well documented.

Performance through simplicity
------------------------------
Once the iterative slicing function is reached the slices are to be simple
native Python slice objects that can be run through a simple lightweight
generator. All preparation of slices is to be done in advance of reaching the
slicing generator functions.

Scalability
-----------
The tools are to be designed to leverage Python generators so that they can
handle big data if necessary.

Object agnostic slicing
-----------------------
If the sequence can be sliced in Python it should be able to be sliced with
this toolkit. Slicing is to be performed without prior knowledge of the
actual object types contained within the sequences.
