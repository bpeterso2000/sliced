import unittest

from sliced.intervals.endpoint import EndPoint


class TestEndPointClass(unittest.TestCase):

    def setUp(self):
        self.endpoint = EndPoint()

    # --- origin setter tests ----

    def test_set_origin_to_zero(self):
        self.endpoint.origin = 0
        self.assertEqual(self.endpoint.origin, 0)

    def test_set_origin_to_one(self):
        self.endpoint.origin = 1
        self.assertEqual(self.endpoint.origin, 1)

    def test_attempt_to_set_invalid_origin(self):
        with self.assertRaises(ValueError):
            EndPoint(origin=2)

    # --- value setter tests ----

    def test_set_to_none(self):
        self.endpoint.value = None
        self.assertIsNone(self.endpoint.value)

    def test_set_to_origin(self):
        self.endpoint.value = 1
        self.assertEqual(self.endpoint.value, 1)

    def test_set_above_origin(self):
        self.endpoint.value = 2
        self.assertEqual(self.endpoint.value, 2)

    def test_set_relative_endpoint(self):
        self.endpoint.value = -1
        self.assertEqual(self.endpoint.value, -1)

    def test_unable_to_convert_to_an_int(self):
        with self.assertRaises(ValueError):
            EndPoint('a')

    # --- add/subtract operator tests ---

    def test_add_endpoint_to_endpoint(self):
        self.endpoint.value = 1
        self.assertEqual((self.endpoint + EndPoint(1)).value, 2)

    def test_increment_endpoint(self):
        self.endpoint.value = 1
        self.assertEqual((self.endpoint + 1).value, 2)

    def test_increment_relative_enpoint_to_zero(self):
        self.endpoint.value = -1
        self.assertIsNone((self.endpoint + 1).value)

    def test_subtract_endpoint_from_endpoint(self):
        self.endpoint.value = 2
        self.assertEqual((self.endpoint - EndPoint(1)).value, 1)

    def test_decrement_endpoint_below_origin(self):
        self.endpoint.value = 2
        self.assertIsNone((self.endpoint - 2).value)

    def test_decrement_unit_based_endpoint_below_origin(self):
        self.endpoint.origin = 0
        self.endpoint.value = 1
        self.assertIsNone((self.endpoint - 2).value)

    def test_decrement_endpoint_to_origin(self):
        self.endpoint.value = 2
        self.assertEqual((self.endpoint - 1).value, 1)

    def test_in_place_add_endpoint(self):
        self.endpoint.value = 1
        self.endpoint += EndPoint(1)
        self.assertEqual(self.endpoint, 2)

    def test_in_place_add_equals_none(self):
        self.endpoint += 1
        self.assertIsNone(self.endpoint.value)

    def test_in_place_add_equals_int_value(self):
        self.endpoint.value = 1
        self.endpoint += 1
        self.assertEqual(self.endpoint.value, 2)

    def test_in_place_subtract_endpoint(self):
        self.endpoint.value = 2
        self.endpoint -= EndPoint(1)
        self.assertEqual(self.endpoint, 1)

    def test_in_place_subtract_equals_none(self):
        self.endpoint -= 1
        self.assertIsNone(self.endpoint.value)

    def test_in_place_sutract_int_value(self):
        self.endpoint.value = -1
        self.endpoint -= 1
        self.assertEqual(self.endpoint.value, -2)

    # --- equality tests ---

    def test_endpoint_equals_endpoint(self):
        self.endpoint.value = 1
        self.assertTrue(self.endpoint == EndPoint(1))

    def test_unbounded_endpoint_equals_an_int(self):
        self.assertIsNone(self.endpoint == 1)

    def test_bounded_endpoint_equality_test_true(self):
        self.endpoint.value = 1
        self.assertTrue(self.endpoint == 1)

    def test_bounded_endpoint_equality_test_false(self):
        self.endpoint.value = 1
        self.assertFalse(self.endpoint == 0)

    # --- not equals tests ---

    def test_endpoint_not_equals_endpoint(self):
        self.endpoint.value = 1
        self.assertTrue(self.endpoint == EndPoint(1))

    def test_unbounded_endpoint_not_equals_an_int(self):
        self.assertFalse(self.endpoint != 1)

    def test_bounded_endpoint_not_equals_test_true(self):
        self.endpoint.value = 1
        self.assertTrue(self.endpoint != 0)

    def test_bounded_endpoint_not_equals_test_false(self):
        self.endpoint.value = 1
        self.assertFalse(self.endpoint != 1)

    # --- not greater than tests ---

    def test_endpoint_greater_than_endpoint(self):
        self.endpoint.value = 1
        self.assertTrue(self.endpoint == EndPoint(1))

    def test_unbounded_endpoint_greater_than_none(self):
        self.assertIsNone(self.endpoint > None)

    def test_unbounded_endpoint_greater_than_an_int(self):
        self.assertFalse(self.endpoint > 1)

    def test_bounded_endpoint_greater_than_a_smaller_value(self):
        self.endpoint.value = 1
        self.assertTrue(self.endpoint > 0)

    def test_bounded_endpoint_greater_than_a_larger_value(self):
        self.endpoint.value = 1
        self.assertFalse(self.endpoint > 2)

    def test_bounded_endpoint_greater_than_an_equal_value(self):
        self.endpoint.value = 1
        self.assertFalse(self.endpoint > 1)

    # --- greater than tests ---

    def test_unbounded_endpoint_greater_than_or_equal_none(self):
        self.assertIsNone(self.endpoint >= None)

    def test_unbounded_endpoint_greater_than_or_equal_an_int(self):
        self.assertFalse(self.endpoint >= 1)

    def test_bounded_endpoint_greater_than_or_equal_a_smaller_value(self):
        self.endpoint.value = 1
        self.assertTrue(self.endpoint >= 0)

    def test_bounded_endpoint_greater_than_or_equal_a_larger_value(self):
        self.endpoint.value = 1
        self.assertFalse(self.endpoint >= 2)

    def test_bounded_endpoint_greater_than_or_equal_an_equal_value(self):
        self.endpoint.value = 1
        self.assertTrue(self.endpoint >= 1)

    # --- less than tests ---

    def test_unbounded_endpoint_less_than_none(self):
        self.assertIsNone(self.endpoint < None)

    def test_unbounded_endpoint_less_than_an_int(self):
        self.assertFalse(self.endpoint < 1)

    def test_bounded_endpoint_less_than_a_smaller_value(self):
        self.endpoint.value = 1
        self.assertFalse(self.endpoint < 0)

    def test_bounded_endpoint_less_than_a_larger_value(self):
        self.endpoint.value = 1
        self.assertTrue(self.endpoint < 2)

    def test_bounded_endpoint_less_than_an_equal_value(self):
        self.endpoint.value = 1
        self.assertFalse(self.endpoint < 1)

    # --- less than equal tests ---

    def test_unbounded_endpoint_less_than_or_equal_none(self):
        self.assertIsNone(self.endpoint <= None)

    def test_unbounded_endpoint_less_than_or_equal_an_int(self):
        self.assertFalse(self.endpoint <= 1)

    def test_bounded_endpoint_less_than_or_equal_a_smaller_value(self):
        self.endpoint.value = 1
        self.assertFalse(self.endpoint <= 0)

    def test_bounded_endpoint_less_than_or_equal_a_larger_value(self):
        self.endpoint.value = 1
        self.assertTrue(self.endpoint <= 2)

    def test_bounded_endpoint_less_than_or_equal_value(self):
        self.endpoint.value = 1
        self.assertTrue(self.endpoint <= 1)

    # --- test absolute/relative properties ---

    def test_absolute_when_endpoint_greater_than_zero(self):
        self.endpoint.value = 1
        self.assertTrue(self.endpoint.absolute)

    def test_is_absolute_when_endpoint_less_than_zero(self):
        self.endpoint.value = -1
        self.assertFalse(self.endpoint.absolute)

    def test_is_absolute_when_endpoint_equals_zero(self):
        self.endpoint.origin = 0
        self.endpoint.value = 0
        self.assertTrue(self.endpoint.absolute)

    def test_relative_when_endpoint_greater_than_zero(self):
        self.endpoint.value = 1
        self.assertFalse(self.endpoint.relative)

    def test_is_relative_when_endpoint_less_than_zero(self):
        self.endpoint.value = -1
        self.assertTrue(self.endpoint.relative)

    def test_is_relative_when_endpoint_equals_zero(self):
        self.endpoint.origin = 0
        self.endpoint.value = 0
        self.assertFalse(self.endpoint.relative)

    # --- test bound/unbound property ---

    def test_is_bound_when_endpoint_none(self):
        self.assertFalse(self.endpoint.bound)

    def test_is_bound_when_endpoint_is_an_int(self):
        self.endpoint.value = 1
        self.assertTrue(self.endpoint.bound)

    def test_is_unbound_when_endpoint_none(self):
        self.assertTrue(self.endpoint.unbound)

    def test_is_unbound_when_endpoint_is_an_int(self):
        self.endpoint.value = 1
        self.assertFalse(self.endpoint.unbound)

    # --- test string representation ---

    def test_print_unbounded_endpoint(self):
        self.assertEqual(str(self.endpoint), 'None (unbound)')

    def test_print_unit_based_endpoint(self):
        self.endpoint.value = 1
        self.assertEqual(str(self.endpoint), '1 (unit-based)')

    def test_print_zero_based_endpoint(self):
        self.endpoint = EndPoint(1, origin=0)
        self.assertEqual(str(self.endpoint), '1 (zero-based)')
