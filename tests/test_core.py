import unittest
from string import ascii_lowercase

from sliced import slice_, slices, cut

class TestCoreFunctions(unittest.TestCase):

    def setUp(self):
        self.seq = [[i + str(j) for j in range(9)]
                    for i in ascii_lowercase[:2]]

    def test_slice_(self):
        self.assertEqual(list(slice_(self.seq, ':3')),
                         [['a0', 'a1', 'a2'], ['b0', 'b1', 'b2']])
        self.assertEqual(list(slice_(self.seq, ':.3', dialect='dot_notation')),
                         [['a0', 'a1'], ['b0', 'b1']])

    def test_slices(self):
        self.assertEqual(list(slices(self.seq, ':3')),
                         [['a0', 'a1', 'a2'], ['b0', 'b1', 'b2']])
        self.assertEqual(list(slices(self.seq, ':.3, 5',
                         dialect='dot_notation')), [['a0', 'a1', 'a4'],
                         ['b0', 'b1', 'b4']])

    def test_cut(self):
        self.assertEqual(list(cut(self.seq, '-3')), [['a0', 'a1', 'a2'],
                         ['b0', 'b1', 'b2']])
        self.assertEqual(list(cut(self.seq, '3-5, 7')),
                         [['a2', 'a3', 'a4', 'a6'], ['b2', 'b3', 'b4', 'b6']])

if __name__ == '__main__':
    unittest.main()
