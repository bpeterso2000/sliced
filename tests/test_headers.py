import unittest

import sliced
from sliced.headers import Headers
from sliced.exceptions import InvalidSliceString

class TestHeaders(unittest.TestCase):

    def test_names_to_indices(self):
        headers = Headers(['col 1', 'col 2', 'c', 'd', 'col 5'])
        text = '`col 2`:`col 5`:2, c, `col 1`'
        self.assertEqual(headers.names_to_indices(text), '2:5:2, 3, 1')

    def test_names_to_zero_based_indices(self):
        headers = Headers(['col 1', 'col 2', 'c', 'd', 'col 5'], origin=0)
        text = '`col 2`:`col 5`:2, c, `col 1`'
        self.assertEqual(headers.names_to_indices(text), '1:4:2, 2, 0')

    def test_case_senstive(self):
        headers = Headers(['col 1', 'col 2', 'c', 'd', 'col 5'])
        text = '`Col 2`:`col 5`:2, c, `col 1`'
        with self.assertRaises(InvalidSliceString):
            headers.names_to_indices(text)

    def test_case_insenstive(self):
        headers = Headers(['col 1', 'col 2', 'c', 'd', 'col 5'],
                          ignorecase=True)
        text = '`Col 2`:`col 5`:2, c, `col 1`'
        self.assertEqual(headers.names_to_indices(text), '2:5:2, 3, 1')

    def test_duplicate_headers(self):
        with self.assertRaises(DuplicateItemsNotAllowed):
            Headers(['col 1', 'col 2', 'c', 'd', 'col 2'])
