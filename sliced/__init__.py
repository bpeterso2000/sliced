"""
    sliced
    ======

    A simple Python slicing toolkit.

    :copyright: (c) 2014 by Brian Peterson.
    :license: Apache 2.0, see LICENSE for more details.
"""
import sliced
from ._compat import *
from . import headers
from . import intervals
from .core import as_list, slice_, slices, cut
from .exceptions import OptionNotFound, InvalidSliceString
from .grammar import Grammar


__all__ = ('as_list', 'slices', 'slice_', 'cut',
           'OptionsNotFound', 'InvalidSliceString',
           'headers', 'intervals')


__version__ = '0.1a'
