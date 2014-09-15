# -*- coding: utf-8 -*-
from .exceptions import EndPointValueError, OriginValueError


class EndPoint(object):
    """
    An unbounded, zero-based or unit-based interval endpoint.

    * Add & subtract operator support for endpoints.  Handles unbounded
      endpoint conditions, zero and unit-based origins and ensures that the
      endpoint values remain sane during the operations.

    * Provides relational operator support for endpoint objects

    Attributes:
      origin (int):  0 or 1
      value (int):   None or integer

    Properties:
      bound (bool):     Endpoint is set (int)
      unbound (bool):   Endpoint not set (-oo or oo)
      absolute (bool):  Endpoint value represents an absolute position (+n)
      relative (bool):  Endpoint relative to the last position in sequence (-n)

    :raises: EndPointValueError, OriginValueError
    """

    def __init__(self, value=None, origin=1):
        self.origin = origin
        self.value = value

    def __add__(self, operand):
        operand_ = operand.value if hasattr(operand, 'value') else operand
        if self.bound and operand_ is not None:
            result = self._value + operand_
            decr_out_of_range = (self.value >= 0 and operand_ < 0
                                 and result < self._origin)
            incr_out_of_range = self.value < 0 and operand_ > 0 and result >= 0
            if not (decr_out_of_range or incr_out_of_range):
                return EndPoint(result, self._origin)
        return EndPoint(None, origin=self._origin)

    def __sub__(self, operand):
        operand_ = operand.value if hasattr(operand, 'value') else operand
        if operand_ is not None:
            operand_ = -operand_
        return self.__add__(operand_)

    def __iadd__(self, operand):
        self._value = self.__add__(operand).value
        return self

    def __isub__(self, operand):
        self._value = self.__sub__(operand).value
        return self

    def _compare(self, comparison, obj):
        value = obj.value if hasattr(obj, 'value') else obj
        if self.unbound or value is None:
            return
        return int.__dict__[comparison](self._value, int(value))

    def __eq__(self, obj):
        return self._compare('__eq__', obj)

    def __ne__(self, obj):
        return self._compare('__ne__', obj)

    def __le__(self, obj):
        return self._compare('__le__', obj)

    def __ge__(self, obj):
        return self._compare('__ge__', obj)

    def __lt__(self, obj):
        return self._compare('__lt__', obj)

    def __gt__(self, obj):
        return self._compare('__gt__', obj)

    def __repr__(self):
        if self.unbound:
            return 'None (unbound)'
        origin = 'unit' if self.origin else 'zero'
        return '{} ({}-based)'.format(self.value, origin)

    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, value):
        try:
            self._origin = int(value)
            if self._origin not in [0, 1]:
                raise ValueError()
        except (ValueError, TypeError):
                raise OriginValueError('Origin must be 0 or 1.')

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value_):
        if value_ is None:
            self._value = None
        else:
            try:
                number = int(value_)
                if number >= 0 and number < self.origin:
                    raise ValueError('Value outside the origin.')
                self._value = number
            except (ValueError, TypeError) as error:
                raise EndPointValueError(error)

    @property
    def bound(self):
        return self.value is not None

    @property
    def unbound(self):
        return not self.bound

    @property
    def absolute(self):
        "Endpoint value represents an absolute position in the sequence"
        return self.bound and self.value >= 0

    @property
    def relative(self):
        """
        Endpoint value is relative to the last position in the sequence:
        * -1 represents the last position
        * -2 represents the 2nd to last position
        * and so on ...
        """
        return not self.absolute
