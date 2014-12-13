import unittest
import pyparsing
import sliced

class TestGrammarClass(unittest.TestCase):

    def setUp(self):
        self.grammar = sliced.Grammar()

    def test_default_dialect(self):
        self.assertEqual(self.grammar.dialect, 'slice_list')
        self.assertEqual(self.grammar.list_sep, ',')
        self.assertEqual(self.grammar.range_sep, ':')
        self.assertEqual(self.grammar.step_sep, ':')
        self.assertTrue(self.grammar.allow_relative_indices)
        self.assertTrue(self.grammar.allow_stepped_intervals)
        self.assertTrue(self.grammar.allow_reverse_strides)
        self.assertTrue(self.grammar.allow_slice_list)
        self.assertEqual(self.grammar.interval, {':': 'closed'})

    def test_set_dialect(self):
        self.grammar.dialect = 'python_slice'
        self.assertEqual(self.grammar.dialect, 'python_slice')
        self.assertFalse(self.grammar.allow_slice_list)
        with self.assertRaises(sliced.UnknownDialect):
            self.grammar.dialect = 'bad dialect'

    def test_allow_relative_indices(self):
        self.assertEqual(list(self.grammar.parse_text('-2')), [{'start': -2}])
        self.grammar.allow_relative_indices = False
        with self.assertRaises(sliced.InvalidSliceString):
            self.grammar.parse_text('-2')

    def test_allow_stepped_intervals(self):
        self.assertEqual(list(self.grammar.parse_text('::2')),
            [{'range_sep': ':', 'step': 2}])
        self.grammar.allow_stepped_intervals = False
        with self.assertRaises(sliced.InvalidSliceString):
            self.grammar.parse_text('::2')

    def test_allow_reverse_strides(self):
        self.assertEqual(list(self.grammar.parse_text('::-1')),
            [{'range_sep': ':', 'step': -1}])
        self.grammar.allow_reverse_strides = False
        with self.assertRaises(sliced.InvalidSliceString):
            self.grammar.parse_text('::-1')

    def test_allow_slice_list(self):
        self.assertEqual(list(self.grammar.parse_text('1, 2')),
                         [{'start': 1}, {'start': 2}])
        self.grammar.allow_slice_list = False
        with self.assertRaises(sliced.InvalidSliceString):
            self.grammar.parse_text('1, 2')

    def test_slice_list_dialect(self):
        self.grammar.dialect = 'slice_list'
        self.assertEqual(list(self.grammar.parse_text('1, 2:5:2, -2')), [
                         {'start': 1},
                         {'start': 2, 'range_sep': ':', 'stop': 5, 'step': 2},
                         {'start': -2}])
        with self.assertRaises(sliced.InvalidSliceString):
            self.grammar.parse_text('1-2')

    def test_python_slice_dialect(self):
        self.grammar.dialect = 'python_slice'
        self.assertEqual(list(self.grammar.parse_text('2:5:2')), [
                         {'start': 2, 'range_sep': ':', 'stop': 5, 'step': 2}])
        with self.assertRaises(sliced.InvalidSliceString):
            self.grammar.parse_text('1, 2:5:2, -2')

    def test_dot_notation_dialect(self):
        self.grammar.dialect = 'dot_notation'
        self.assertEqual(list(self.grammar.parse_text('1, 2:5:2')), [
                         {'start': 1}, {'start': 2, 'range_sep': ':',
                          'stop': 5, 'step': 2}])
        self.assertEqual(list(self.grammar.parse_text('1, 2.:5:2')), [
                         {'start': 1}, {'start': 2, 'range_sep': '.:',
                          'stop': 5, 'step': 2}])
        self.assertEqual(list(self.grammar.parse_text('1, 2.:.5:2')), [
                         {'start': 1}, {'start': 2, 'range_sep': '.:.',
                          'stop': 5, 'step': 2}])
        self.assertEqual(list(self.grammar.parse_text('1, 2:.5:2')), [
                         {'start': 1}, {'start': 2, 'range_sep': ':.',
                          'stop': 5, 'step': 2}])
        self.assertEqual(list(self.grammar.parse_text('1, 2..5:2')), [
                         {'start': 1}, {'start': 2, 'range_sep': '..',
                          'stop': 5, 'step': 2}])
        with self.assertRaises(sliced.InvalidSliceString):
            self.grammar.parse_text('1, 2...5:2, -2')

    def test_unix_cut(self):
        self.grammar.dialect = 'unix_cut'
        self.assertEqual(list(self.grammar.parse_text('2-5, 8')), [
                         {'start': 2, 'range_sep': '-', 'stop': 5},
                         {'start': 8}])
        with self.assertRaises(sliced.InvalidSliceString):
            self.grammar.parse_text('1:2')

    def test_to_int(self):
        self.assertEqual(self.grammar._to_int(['2']), 2)

    def test_get_dialects(self):
        self.assertEqual(set(self.grammar.get_dialects()), {'slice_list',
            'python_slice', 'dot_notation', 'double_dot', 'unix_cut'})

    def test_list_dialects(self):
        self.assertIn('slice_list', self.grammar.list_dialects())
        self.assertIn('python_slice', self.grammar.list_dialects())
        self.assertIn('dot_notation', self.grammar.list_dialects())
        self.assertIn('double_dot', self.grammar.list_dialects())
        self.assertIn('unix_cut', self.grammar.list_dialects())


    def test_validate_separators(self):
        self.assertTrue(self.grammar.validate_separators())
        self.grammar.range_sep = 'a'
        with self.assertRaises(sliced.InvalidSeparator):
            self.grammar.validate_separators()
        self.grammar.range_sep = ':'
        self.assertTrue(self.grammar.validate_separators())
        self.grammar.step_sep = 'a'
        with self.assertRaises(sliced.InvalidSeparator):
            self.grammar.validate_separators()
        self.grammar.step_sep = ':'
        self.assertTrue(self.grammar.validate_separators())
        self.grammar.list_sep = 'a'
        with self.assertRaises(sliced.InvalidSeparator):
            self.grammar.validate_separators()

    def test_get_slice_item(self):
        grammar = self.grammar._get_slice_item() + pyparsing.stringEnd
        self.assertEqual(grammar.parseString('2').asList(), ['2'])
        self.assertEqual(grammar.parseString('2:3').asList(), ['2:3'])
        self.assertEqual(grammar.parseString('2:3:4').asList(), ['2:3:4'])
        self.grammar.allow_stepped_intervals = False
        grammar = self.grammar._get_slice_item() + pyparsing.stringEnd
        self.assertEqual(grammar.parseString('2').asList(), ['2'])
        self.assertEqual(grammar.parseString('2:3').asList(), ['2:3'])
        with self.assertRaises(pyparsing.ParseException):
            grammar.parseString('2:3:4')

    def test_get_slice_list(self):
       grammar = self.grammar._get_slice_list() + pyparsing.stringEnd
       self.assertEqual(grammar.parseString('2, 3').asList(), ['2', '3'])
       self.assertEqual(grammar.parseString('2,3,').asList(), ['2', '3'])
       self.assertEqual(grammar.parseString('2:3:4').asList(), ['2:3:4'])
       self.assertEqual(grammar.parseString('2, 2:3:4, 6').asList(),
                        ['2', '2:3:4', '6'])


if __name__ == '__main__':
    unittest.main()
