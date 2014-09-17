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
from .core import slice_, slices, cut
from .endpoint import EndPoint
from .exceptions import OriginValueError, \
    EndPointValueError, EndPointZeroNotAllowed, \
    InvalidIntervalType, InvalidStepSize, InvalidSliceString
    
from .grammar import Grammar
from .interval import Interval


__all__ = [
    'slices', 'slice_', 'cut',
    'EndPoint', 'Interval', 'Grammar',
    'EndPointValueError', 'EndPointZeroNotAllowed', 'OriginValueError',
    'InvalidIntervalType', 'InvalidStepSize', 'InvalidSliceString',
]


__version__ = '0.5'
