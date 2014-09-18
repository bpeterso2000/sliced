# -*- coding: utf-8 -*-
import math

from ._compat import STRING_TYPES
from .endpoint import EndPoint
from .exceptions import InvalidIntervalType, InvalidStepSize


class Interval(object):
    "http://en.wikipedia.org/wiki/Interval_(mathematics)"
    types = ['closed', 'right-open', 'left-open', 'open']

    def __init__(self, start=None, stop=None, step=None,
                 type_='closed', origin=1):
        """
        :param start: lower bound (default: None -- unbounded)
        :param stop: upper bound (default: None -- unbounded)
        :param step: stride (default: None -- step size 1)
        :param origin:
            * 0: zero-based
            * 1: unit-based
        :param type_:
            * 'closed'      [start, stop]
            * 'left-open'   (start, stop]
            * 'right-open'  [start, stop)
            * 'open'        (start, stop)
            *  or if you prefer use a 2-bit binary number:
                left-bit: if set the left-side of interval is open
                right-bit: if set the right-side of interval is open
        :raises:
            EndPointValueError
            OriginValueError
            InvalidIntervalType
            InvalidStepSize
        """
        self.type = type_
        self.origin = int(origin)
        self.set(start, stop, step)

        for value, type_ in enumerate(self.__class__.types):
            self.__dict__[type_.replace('-', '_').upper()] = value

    def __repr__(self):
        left_brace = '(' if self.left_open else '['
        right_brace = ')' if self.right_open else ']'
        start = self.lower_bound if self.left_bounded else '-oo'
        stop = self.upper_bound if self.right_bounded else '+oo'
        step = '' if self.stride is None else ' step {}'
        return '{}{}, {}{}'.format(left_brace, start, stop, right_brace, step)

    @property
    def lower_bound(self):
        return self._lower_bound.value

    @lower_bound.setter
    def lower_bound(self, value):
        self._lower_bound = EndPoint(value, self.origin)

    @property
    def upper_bound(self):
        return self._upper_bound.value

    @upper_bound.setter
    def upper_bound(self, value):
        self._upper_bound = EndPoint(value, self.origin)

    @property
    def type(self):
        return self.__class__.types[self._type]

    @type.setter
    def type(self, value):
        """
        :returns: 2-bit binary value representing the interval type,
            left bit set -> interval is left-open,
            right bit set -> interval is right-open.
        """
        self._type = self._get_type(value)

    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, value):
        if hasattr(self, '_lower_bound'):
            self._lower_bound.origin = value
            self._upper_bound.origin = value
        self._origin = value

    @property
    def endpoints(self):
        return (self._lower_bound, self._upper_bound)

    @property
    def degenerate(self):
        start, stop = self.to_closed()
        return self.bounded and (start == stop)

    @property
    def empty(self):
        start, stop = self.to_closed()
        return self.bounded and (start > stop)

    @property
    def proper(self):
        return not (self.empty or self.degenerate)

    @property
    def unbounded(self):
        return not self.bounded

    @property
    def left_bounded(self):
        return self.lower_bound is not None

    @property
    def right_bounded(self):
        return self.upper_bound is not None

    @property
    def bounded(self):
        return self.left_bounded and self.right_bounded

    @property
    def open(self):
        return self.left_open and self.right_open

    @property
    def half_open(self):
        return self.left_open != self.right_open

    @property
    def left_open(self):
        return bool(self._type & self.LEFT_OPEN)

    @property
    def right_open(self):
        return bool(self._type & self.RIGHT_OPEN)

    @property
    def left_closed(self):
        return not self.left_open

    @property
    def right_closed(self):
        return not self.right_open

    @property
    def half_closed(self):
        return self.half_open

    @property
    def closed(self):
        return self.left_closed and self.right_closed

    @property
    def reversed(self):
        return self.stride is not None and self.stride < 0

    @staticmethod
    def _sign(number):
        ":returns: sign of number (-1 or +1)"
        return +1 if number is None else int(math.copysign(1, float(number)))

    def _get_direction(self, stride=False):
        "+1 for None or positive step (aka stride), -1 for negative step"
        if stride is False:
            stride = self.stride
        return 1 if stride is None else self.__class__._sign(stride)

    def _get_endpoints(self, start=False, stop=False, origin=False):
            if isinstance(start, EndPoint):
                if origin is False:
                    origin = start.origin
                start = start.value
            if isinstance(stop, EndPoint):
                if origin is False:
                    origin = stop.origin
                stop = stop.value
            if start is False and stop is False:
                start, stop = self._lower_bound.value, self._upper_bound.value
            elif start is False:
                start, stop = None, stop
            elif stop is False:
                start, stop = start, None
            origin = self.origin if origin is False else origin
            return EndPoint(start, origin), EndPoint(stop, origin)

    def _get_new_origin(self, new_origin, start=False, stop=False):
        start, stop = self._get_endpoints(start, stop, new_origin)
        if new_origin != self.origin:
            if start.absolute:
                start += new_origin - self.origin
            if stop.absolute:
                stop += new_origin - self.origin
        return start, stop

    def _get_new_type(self, new_type, start=False, stop=False, step=False,
                      old_type=False, to_origin=False):
            start, stop = self._get_endpoints(start, stop)
            if not (to_origin is False or to_origin == self.origin):
                start, stop = self._get_new_origin(to_origin, start, stop)
            direction = self._get_direction(step)
            new_type = self._get_type(new_type)
            old_type = (self._type if old_type is False
                        else self._get_type(old_type))
            if (old_type ^ new_type) & self.LEFT_OPEN:
                is_old_left_open = self._is_left_open(old_type)
                is_new_left_open = self._is_left_open(new_type)
                start += (is_old_left_open - is_new_left_open) * direction
            if (old_type ^ new_type) & self.RIGHT_OPEN:
                is_old_right_open = self._is_right_open(old_type)
                is_new_right_open = self._is_right_open(new_type)
                stop += (is_new_right_open - is_old_right_open) * direction
            return start, stop

    def _get_type(self, value):
        if isinstance(value, STRING_TYPES):
            interval = value.replace('_', '-').replace(' ', '-')
            try:
                return self.__class__.types.index(interval)
            except (IndexError, TypeError, ValueError) as error:
                raise InvalidIntervalType(error, self.__class__.types)
        try:
            value = int(value)
            if value < 0 or value > 3:
                InvalidIntervalType('Invalid 2-bit binary number.')
        except (TypeError, ValueError) as error:
            raise InvalidIntervalType(error)
        return value

    def _is_left_open(self, type_):
        return (type_ & self.LEFT_OPEN) >> 1

    def _is_right_open(self, type_):
        return (type_ & self.RIGHT_OPEN)

    def _set_step(self, value):
            try:
                step = int(value)
                if step == 0:
                    error_mesg = 'Zero is not a valid step size.'
                    raise InvalidStepSize(error_mesg)
            except (TypeError, ValueError) as error:
                raise InvalidStepSize(error)
            return step

    def set(self, start=None, stop=None, step=None):
        "Set interval endpoints & step size"
        self.lower_bound = start
        self.upper_bound = stop
        self.stride = None if step is None else self._set_step(step)

    def to_zero_based(self, start=False, stop=False):
        "to Python developer friendly zero-based indexing (origin=0)"
        return self._get_new_origin(0, start, stop)

    def to_unit_based(self, start=False, stop=False):
        "to command-line user friendly unit-based indexing (origin=1)"
        return self._get_new_origin(1, start, stop)

    def to_open(self, start=False, stop=False, step=False,
                from_type=False, to_origin=False):
        return self._get_new_type(self.OPEN, start, stop, step,
                                  from_type, to_origin)

    def to_right_open(self, start=False, stop=False, step=False,
                      from_type=False, to_origin=False):
        return self._get_new_type(self.RIGHT_OPEN, start, stop, step,
                                  from_type, to_origin)

    def to_left_open(self, start=False, stop=False, step=False,
                     from_type=False, to_origin=False):
        return self._get_new_type(self.LEFT_OPEN, start, stop, step,
                                  from_type, to_origin)

    def to_closed(self, start=False, stop=False, step=False,
                  from_type=False, to_origin=False):
        return self._get_new_type(self.CLOSED, start, stop, step,
                                  from_type, to_origin)

    def to_slice(self, start=False, stop=False, step=False, from_type=False):
        "to Python slice object"
        if step is False:
            step = self.stride
        start, stop = self.to_right_open(start, stop, step, from_type, 0)
        return slice(start.value, stop.value, step)
