"""
    sliced
    ======

    A simple Python slicing toolkit.

    :copyright: (c) 2014 by Brian Peterson.
    :license: Apache 2.0, see LICENSE for more details.
"""

from __future__ import print_function

import sliced
from ._compat import STRING_TYPES
from .core import get_slice, sliced, cut
from .endpoint import EndPoint
from .exceptions import EndPointValueError, OriginValueError, \
    InvalidIntervalType, InvalidStepSize, InvalidSliceString
from .grammar import Grammar
from .interval import Interval


__version__ = '0.5'

