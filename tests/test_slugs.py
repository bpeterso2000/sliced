import unittest

from sliced.headers.slugs import Slugs, slugify

class TestSlugs(unittest.TestCase):

    def setUp(self):
        self.slugs = Slugs([' Afghanistan+ ', 'Albaine', 'Algérie', 'Albaine'])

    def test_trim(self):
        self.assertEqual(tuple(self.slugs.trim().names)[0], ('Afghanistan+'))

    def test_lowercase(self):
        self.assertEqual(tuple(self.slugs.lowercase().names)[1], ('albaine'))

    def test_deaccent(self):
        self.assertEqual(tuple(self.slugs.deaccent().names)[2], ('Algerie'))

    def test_sub(self):
        result = self.slugs.sub(r'\sA', 'a').names
        self.assertEqual(tuple(result)[0], ('afghanistan+ '))

    def test_replace(self):
        result = self.slugs.replace(' A', 'a').names
        self.assertEqual(tuple(result)[0], ('afghanistan+ '))
        # test with count

    def test_whitespace(self):
        result = self.slugs.whitespace('-').names
        self.assertEqual(tuple(result)[0], ('-Afghanistan+-'))

    def test_nonalphanums(self):
        result = self.slugs.nonalphanums('').names
        self.assertEqual(tuple(result)[0], ('Afghanistan'))

    def test_numdups(self):
        result = self.slugs.numdups().names
        self.assertEqual(tuple(result)[1], ('Albaine-1'))
        self.assertEqual(tuple(result)[3], ('Albaine-2'))

    def test_as_dict(self):
        self.slugs.lowercase()
        self.assertEqual(self.slugs.as_dict()[' afghanistan+ '],
                         ' Afghanistan+ ')

    def test_slugify(self):
        names = slugify(self.slugs.names)
        self.assertEqual(names, {
            'afghanistan': ' Afghanistan+ ',
            'albaine-2': 'Albaine',
            'algerie': 'Alg\u00E9rie',
            'albaine-1': 'Albaine'})

