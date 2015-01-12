"""
    sliced
    ======

    A simple Python slicing toolkit.

    :copyright: (c) 2014 by Brian Peterson.
    :license: Apache 2.0, see LICENSE for more details.
"""
import sliced
from ._compat import *
from .core import as_list, slice_, slices, cut
from .exceptions import OptionNotFound, InvalidSliceString
from .grammar import Grammar
from .headers.header import Headers
from .headers.alphaids import num2id, id2num, get_ids
from .headers.slugs import Slugs, slugify
from .intervals.interval import Interval
from .intervals.interval import EndPoint


__all__ = [
    'slices', 'slice_', 'cut',
    'EndPoint', 'Interval', 'Grammar', 'Header', 'Slug'
    'OptionsNotFound', 'InvalidSliceString'
]

__version__ = '0.1a'
