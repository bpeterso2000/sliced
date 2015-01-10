# -*- coding: utf-8 -*-

import unittest

import sliced
from sliced.exceptions import EndPointValueError, InvalidIntervalType, \
    InvalidStepSize


class TestIntervalClass(unittest.TestCase):

    def setUp(self):
        self.interval = sliced.Interval()

    def test_set_type_closed(self):
        self.interval.type = 'closed'
        self.assertEqual(self.interval.type, 'closed')

    def test_set_type_left_open(self):
        self.interval.type = 'left_open'
        self.assertEqual(self.interval.type, 'left-open')

    def test_set_type_right_open(self):
        self.interval.type = 'right_open'
        self.assertEqual(self.interval.type, 'right-open')

    def test_set_type_open(self):
        self.interval.type = 'open'
        self.assertEqual(self.interval.type, 'open')

    def test_set_invalid_type(self):
        with self.assertRaises(InvalidIntervalType):
            self.interval.type = 'broken'

    def test_set_origin(self):
        self.interval.origin = 1
        self.assertEqual(self.interval.origin, 1)
        self.assertEqual(self.interval._lower_bound.origin, 1)
        self.assertEqual(self.interval._upper_bound.origin, 1)

    def test_set(self):
        self.interval.set(start=2, stop=5, step=2)
        self.assertEqual(self.interval._lower_bound.value, 2)
        self.assertEqual(self.interval._upper_bound.value, 5)
        self.assertEqual(self.interval.stride, 2)

    def to_zero_based_endpoints(self):
        interval = sliced.Interval(start=2, stop=5)
        self.assertEqual(interval.to_zero_based_endpoints(), (1, 4))

    def to_unit_based_endpoints(self):
        interval = sliced.Interval(start=2, stop=5, origin=0)
        self.assertEqual(interval.to_zero_based_endpoints(), (3, 6))

    def test_set_invalid_step(self):
        with self.assertRaises(InvalidStepSize):
            self.interval.set(step='a')

    def test_to_open(self):
        self.assertEqual(self.interval.to_open(start=2, stop=5),
                         (1, 6))
        self.assertEqual(self.interval.to_open(start=2, stop=5,
                         from_type='right-open'), (1, 5))

    def test_to_right_open(self):
        self.assertEqual(self.interval.to_right_open(start=2, stop=5),
                         (2, 6))
        self.assertEqual(self.interval.to_right_open(start=2, stop=5,
                         from_type='open'), (3, 5))

    def test_to_left_open(self):
        self.assertEqual(self.interval.to_left_open(start=2, stop=5),
                         (1, 5))
        self.assertEqual(self.interval.to_left_open(start=2, stop=5,
                         from_type='right-open'), (1, 4))

    def test_to_closed(self):
        self.assertEqual(self.interval.to_closed(start=2, stop=5),
                         (2, 5))
        self.assertEqual(self.interval.to_closed(start=2, stop=5,
                         from_type='right-open'), (2, 4))

    def test_to_slice(self):
        self.assertEqual(self.interval.to_slice(start=2, stop=5), slice(1, 5))
        self.assertEqual(self.interval.to_slice(start=2, stop=5,
                         from_type='open'), slice(2, 4, None))

    def test_is_degenerate(self):
        self.assertFalse(self.interval.degenerate)
        self.assertFalse(sliced.Interval(stop=1).degenerate)
        self.assertFalse(sliced.Interval(1).degenerate)
        self.assertTrue(sliced.Interval(1, 1).degenerate)
        self.assertTrue(sliced.Interval(-1, -1).degenerate)

    def test_is_proper(self):
        self.assertTrue(self.interval.proper)
        self.assertFalse(sliced.Interval(2, 1).proper)
        self.assertTrue(sliced.Interval(1).proper)
        self.assertFalse(sliced.Interval(1, 1).proper)
        self.assertFalse(sliced.Interval(-1, -1).proper)

    def test_is_empty(self):
        self.assertFalse(self.interval.empty)
        self.assertTrue(sliced.Interval(2, 1).empty)
        self.assertFalse(sliced.Interval(1).empty)
        self.assertFalse(sliced.Interval(1, 1).empty)
        self.assertFalse(sliced.Interval(-1, -1).empty)

    def test_is_unbounded(self):
        self.assertTrue(self.interval.unbounded)
        self.assertTrue(sliced.Interval(1).unbounded)
        self.assertTrue(sliced.Interval(1).unbounded)
        self.assertFalse(sliced.Interval(1, 1).unbounded)
        self.assertFalse(sliced.Interval(-1, -1).unbounded)

    def test_test_is_left_bounded(self):
        self.assertFalse(self.interval.left_bounded)
        self.assertFalse(sliced.Interval(stop=1).left_bounded)
        self.assertTrue(sliced.Interval(1).left_bounded)
        self.assertTrue(sliced.Interval(1, 1).left_bounded)
        self.assertTrue(sliced.Interval(-1, -1).left_bounded)

    def test_is_right_bounded(self):
        self.assertFalse(self.interval.right_bounded)
        self.assertTrue(sliced.Interval(stop=1).right_bounded)
        self.assertFalse(sliced.Interval(1).right_bounded)
        self.assertTrue(sliced.Interval(1, 1).right_bounded)
        self.assertTrue(sliced.Interval(-1, -1).right_bounded)

    def test_is_bounded(self):
        self.assertFalse(self.interval.bounded)
        self.assertFalse(sliced.Interval(stop=1).bounded)
        self.assertFalse(sliced.Interval(1).bounded)
        self.assertTrue(sliced.Interval(1, 1).bounded)
        self.assertTrue(sliced.Interval(-1, -1).bounded)

    def test_is_left_open(self):
        self.assertTrue(sliced.Interval(type_='open').left_open)
        self.assertTrue(sliced.Interval(type_='left-open').left_open)
        self.assertFalse(sliced.Interval(type_='right-open').left_open)
        self.assertFalse(sliced.Interval(type_='closed').left_open)

    def test_is_right_open(self):
        self.assertTrue(sliced.Interval(type_='open').right_open)
        self.assertFalse(sliced.Interval(type_='left-open').right_open)
        self.assertTrue(sliced.Interval(type_='right-open').right_open)
        self.assertFalse(sliced.Interval(type_='closed').right_open)

    def test_is_left_closed(self):
        self.assertFalse(sliced.Interval(type_='open').left_closed)
        self.assertFalse(sliced.Interval(type_='left-open').left_closed)
        self.assertTrue(sliced.Interval(type_='right-open').left_closed)
        self.assertTrue(sliced.Interval(type_='closed').left_closed)

    def test_is_right_closed(self):
        self.assertFalse(sliced.Interval(type_='open').right_closed)
        self.assertTrue(sliced.Interval(type_='left-open').right_closed)
        self.assertFalse(sliced.Interval(type_='right-open').right_closed)
        self.assertTrue(sliced.Interval(type_='closed').right_closed)

    def test_is_half_open(self):
        self.assertFalse(sliced.Interval(type_='open').half_open)
        self.assertTrue(sliced.Interval(type_='left-open').half_open)
        self.assertTrue(sliced.Interval(type_='right-open').half_open)
        self.assertFalse(sliced.Interval(type_='closed').half_open)

    def test_is_half_closed(self):
        self.assertFalse(sliced.Interval(type_='open').half_closed)
        self.assertTrue(sliced.Interval(type_='left-open').half_closed)
        self.assertTrue(sliced.Interval(type_='right-open').half_closed)
        self.assertFalse(sliced.Interval(type_='closed').half_closed)

    def test_is_open(self):
        self.assertTrue(sliced.Interval(type_='open').open)
        self.assertFalse(sliced.Interval(type_='left-open').open)
        self.assertFalse(sliced.Interval(type_='right-open').open)
        self.assertFalse(sliced.Interval(type_='closed').open)

    def test_is_closed(self):
        self.assertFalse(sliced.Interval(type_='open').closed)
        self.assertFalse(sliced.Interval(type_='left-open').closed)
        self.assertFalse(sliced.Interval(type_='right-open').closed)
        self.assertTrue(sliced.Interval(type_='closed').closed)

    def test_zero_based_open_slice(self):
        interval = sliced.Interval(origin=0, type_='open')
        self.assertEqual(interval.to_slice(-2, -1), slice(-1, -1, None))
        self.assertEqual(interval.to_slice(-2), slice(-1, None, None))
        self.assertEqual(interval.to_slice(-1, -1), slice(None, -1, None))
        self.assertEqual(interval.to_slice(-1), slice(None, None, None))
        self.assertEqual(interval.to_slice(0, 0), slice(1, 0, None))
        self.assertEqual(interval.to_slice(0, 1), slice(1, 1, None))
        self.assertEqual(interval.to_slice(0, 2), slice(1, 2, None))
        self.assertEqual(interval.to_slice(0), slice(1, None, None))
        self.assertEqual(interval.to_slice(1, 1), slice(2, 1, None))
        self.assertEqual(interval.to_slice(1, 2), slice(2, 2, None))
        self.assertEqual(interval.to_slice(1), slice(2, None, None))
        self.assertEqual(interval.to_slice(2), slice(3, None, None))
        self.assertEqual(interval.to_slice(stop=-2), slice(None, -2, None))
        self.assertEqual(interval.to_slice(stop=-1), slice(None, -1, None))
        self.assertEqual(interval.to_slice(stop=0), slice(None, 0, None))
        self.assertEqual(interval.to_slice(stop=1), slice(None, 1, None))
        self.assertEqual(interval.to_slice(stop=2), slice(None, 2, None))
        self.assertEqual(interval.to_slice(step=3), slice(None, None, 3))

    def test_zero_based_left_open_slice(self):
        interval = sliced.Interval(origin=0, type_='left-open')
        self.assertEqual(interval.to_slice(-2, -1), slice(-1, None, None))
        self.assertEqual(interval.to_slice(-2), slice(-1, None, None))
        self.assertEqual(interval.to_slice(-1, -1), slice(None, None, None))
        self.assertEqual(interval.to_slice(-1), slice(None, None, None))
        self.assertEqual(interval.to_slice(0, 0), slice(1, 1, None))
        self.assertEqual(interval.to_slice(0, 1), slice(1, 2, None))
        self.assertEqual(interval.to_slice(0, 2), slice(1, 3, None))
        self.assertEqual(interval.to_slice(0), slice(1, None, None))
        self.assertEqual(interval.to_slice(1, 1), slice(2, 2, None))
        self.assertEqual(interval.to_slice(1, 2), slice(2, 3, None))
        self.assertEqual(interval.to_slice(1), slice(2, None, None))
        self.assertEqual(interval.to_slice(2), slice(3, None, None))
        self.assertEqual(interval.to_slice(stop=-2), slice(None, -1, None))
        self.assertEqual(interval.to_slice(stop=-1), slice(None, None, None))
        self.assertEqual(interval.to_slice(stop=0), slice(None, 1, None))
        self.assertEqual(interval.to_slice(stop=1), slice(None, 2, None))
        self.assertEqual(interval.to_slice(stop=2), slice(None, 3, None))
        self.assertEqual(interval.to_slice(step=3), slice(None, None, 3))

    def test_zero_based_right_open_slice(self):
        interval = sliced.Interval(origin=0, type_='right-open')
        self.assertEqual(interval.to_slice(-2, -1), slice(-2, -1, None))
        self.assertEqual(interval.to_slice(-2), slice(-2, None, None))
        self.assertEqual(interval.to_slice(-1, -1), slice(-1, -1, None))
        self.assertEqual(interval.to_slice(-1), slice(-1, None, None))
        self.assertEqual(interval.to_slice(0, 0), slice(0, 0, None))
        self.assertEqual(interval.to_slice(0, 1), slice(0, 1, None))
        self.assertEqual(interval.to_slice(0, 2), slice(0, 2, None))
        self.assertEqual(interval.to_slice(0), slice(0, None, None))
        self.assertEqual(interval.to_slice(1, 1), slice(1, 1, None))
        self.assertEqual(interval.to_slice(1, 2), slice(1, 2, None))
        self.assertEqual(interval.to_slice(1), slice(1, None, None))
        self.assertEqual(interval.to_slice(2), slice(2, None, None))
        self.assertEqual(interval.to_slice(stop=-2), slice(None, -2, None))
        self.assertEqual(interval.to_slice(stop=-1), slice(None, -1, None))
        self.assertEqual(interval.to_slice(stop=0), slice(None, 0, None))
        self.assertEqual(interval.to_slice(stop=1), slice(None, 1, None))
        self.assertEqual(interval.to_slice(stop=2), slice(None, 2, None))
        self.assertEqual(interval.to_slice(step=3), slice(None, None, 3))

    def test_zero_based_closed_slice(self):
        interval = sliced.Interval(origin=0, type_='closed')
        self.assertEqual(interval.to_slice(-2, -1), slice(-2, None, None))
        self.assertEqual(interval.to_slice(-2), slice(-2, None, None))
        self.assertEqual(interval.to_slice(-1, -1), slice(-1, None, None))
        self.assertEqual(interval.to_slice(-1), slice(-1, None, None))
        self.assertEqual(interval.to_slice(0, 0), slice(0, 1, None))
        self.assertEqual(interval.to_slice(0, 1), slice(0, 2, None))
        self.assertEqual(interval.to_slice(0, 2), slice(0, 3, None))
        self.assertEqual(interval.to_slice(0), slice(0, None, None))
        self.assertEqual(interval.to_slice(1, 1), slice(1, 2, None))
        self.assertEqual(interval.to_slice(1, 2), slice(1, 3, None))
        self.assertEqual(interval.to_slice(1), slice(1, None, None))
        self.assertEqual(interval.to_slice(2), slice(2, None, None))
        self.assertEqual(interval.to_slice(stop=-2), slice(None, -1, None))
        self.assertEqual(interval.to_slice(stop=-1), slice(None, None, None))
        self.assertEqual(interval.to_slice(stop=0), slice(None, 1, None))
        self.assertEqual(interval.to_slice(stop=1), slice(None, 2, None))
        self.assertEqual(interval.to_slice(stop=2), slice(None, 3, None))
        self.assertEqual(interval.to_slice(step=3), slice(None, None, 3))

    def test_unit_based_open_slice(self):
        interval = sliced.Interval(type_='open')
        self.assertEqual(interval.to_slice(-2, -1), slice(-1, -1, None))
        self.assertEqual(interval.to_slice(-2), slice(-1, None, None))
        self.assertEqual(interval.to_slice(-1, -1), slice(None, -1, None))
        self.assertEqual(interval.to_slice(-1), slice(None, None, None))
        with self.assertRaises(EndPointValueError):
            interval.to_slice(0, 0)
        with self.assertRaises(EndPointValueError):
            interval.to_slice(0, 1)
        with self.assertRaises(EndPointValueError):
            interval.to_slice(0)
        self.assertEqual(interval.to_slice(1, 1), slice(1, 0, None))
        self.assertEqual(interval.to_slice(1, 2), slice(1, 1, None))
        self.assertEqual(interval.to_slice(1), slice(1, None, None))
        self.assertEqual(interval.to_slice(2), slice(2, None, None))
        self.assertEqual(interval.to_slice(stop=-2), slice(None, -2, None))
        self.assertEqual(interval.to_slice(stop=-1), slice(None, -1, None))
        with self.assertRaises(EndPointValueError):
            interval.to_slice(stop=0)
        self.assertEqual(interval.to_slice(stop=1), slice(None, 0, None))
        self.assertEqual(interval.to_slice(stop=2), slice(None, 1, None))
        self.assertEqual(interval.to_slice(step=3), slice(None, None, 3))

    def test_unit_based_left_open_slice(self):
        interval = sliced.Interval(type_='left-open')
        self.assertEqual(interval.to_slice(-2, -1), slice(-1, None, None))
        self.assertEqual(interval.to_slice(-2), slice(-1, None, None))
        self.assertEqual(interval.to_slice(-1, -1), slice(None, None, None))
        self.assertEqual(interval.to_slice(-1), slice(None, None, None))
        with self.assertRaises(EndPointValueError):
            interval.to_slice(0, 0)
        with self.assertRaises(EndPointValueError):
            interval.to_slice(0, 1)
        with self.assertRaises(EndPointValueError):
            interval.to_slice(0)
        self.assertEqual(interval.to_slice(1, 1), slice(1, 1, None))
        self.assertEqual(interval.to_slice(1, 2), slice(1, 2, None))
        self.assertEqual(interval.to_slice(1), slice(1, None, None))
        self.assertEqual(interval.to_slice(2), slice(2, None, None))
        self.assertEqual(interval.to_slice(stop=-2), slice(None, -1, None))
        self.assertEqual(interval.to_slice(stop=-1), slice(None, None, None))
        with self.assertRaises(EndPointValueError):
            interval.to_slice(stop=0)
        self.assertEqual(interval.to_slice(stop=1), slice(None, 1, None))
        self.assertEqual(interval.to_slice(stop=2), slice(None, 2, None))
        self.assertEqual(interval.to_slice(step=3), slice(None, None, 3))

    def test_unit_based_right_open_slice(self):
        interval = sliced.Interval(type_='right-open')
        self.assertEqual(interval.to_slice(-2, -1), slice(-2, -1, None))
        self.assertEqual(interval.to_slice(-2), slice(-2, None, None))
        self.assertEqual(interval.to_slice(-1, -1), slice(-1, -1, None))
        self.assertEqual(interval.to_slice(-1), slice(-1, None, None))
        with self.assertRaises(EndPointValueError):
            interval.to_slice(0, 0)
        with self.assertRaises(EndPointValueError):
            interval.to_slice(0, 1)
        with self.assertRaises(EndPointValueError):
            interval.to_slice(0)
        self.assertEqual(interval.to_slice(1, 1), slice(0, 0, None))
        self.assertEqual(interval.to_slice(1, 2), slice(0, 1, None))
        self.assertEqual(interval.to_slice(1), slice(0, None, None))
        self.assertEqual(interval.to_slice(2), slice(1, None, None))
        self.assertEqual(interval.to_slice(stop=-2), slice(None, -2, None))
        self.assertEqual(interval.to_slice(stop=-1), slice(None, -1, None))
        with self.assertRaises(EndPointValueError):
            interval.to_slice(stop=0)
        self.assertEqual(interval.to_slice(stop=1), slice(None, 0, None))
        self.assertEqual(interval.to_slice(stop=2), slice(None, 1, None))
        self.assertEqual(interval.to_slice(step=3), slice(None, None, 3))

    def test_unit_based_closed_slice(self):
        interval = sliced.Interval(type_='closed')
        self.assertEqual(interval.to_slice(-2, -1), slice(-2, None, None))
        self.assertEqual(interval.to_slice(-2), slice(-2, None, None))
        self.assertEqual(interval.to_slice(-1, -1), slice(-1, None, None))
        self.assertEqual(interval.to_slice(-1), slice(-1, None, None))
        with self.assertRaises(EndPointValueError):
            interval.to_slice(0, 0)
        with self.assertRaises(EndPointValueError):
            interval.to_slice(0, 1)
        with self.assertRaises(EndPointValueError):
            interval.to_slice(0)
        self.assertEqual(interval.to_slice(1, 1), slice(0, 1, None))
        self.assertEqual(interval.to_slice(1, 2), slice(0, 2, None))
        self.assertEqual(interval.to_slice(1), slice(0, None, None))
        self.assertEqual(interval.to_slice(2), slice(1, None, None))
        self.assertEqual(interval.to_slice(stop=-2), slice(None, -1, None))
        self.assertEqual(interval.to_slice(stop=-1), slice(None, None, None))
        with self.assertRaises(EndPointValueError):
            interval.to_slice(stop=0)
        self.assertEqual(interval.to_slice(stop=1), slice(None, 1, None))
        self.assertEqual(interval.to_slice(stop=2), slice(None, 2, None))
        self.assertEqual(interval.to_slice(step=3), slice(None, None, 3))
