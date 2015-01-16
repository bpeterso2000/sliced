import re
import sys
from collections import Counter

from unidecode import unidecode


class Slugs:

    def __init__(self, names):
        self.names = self.orig_names = names
        self.WHITESPACE = re.compile(r'\s+')
        self.NONALPHANUM = re.compile(r'[^\w_-]')

    def trim(self, chars=None):
       self.names = [i.strip(chars) for i in self.names]
       return self

    def lowercase(self):
       self.names = [i.lower() for i in self.names]
       return self

    def deaccent(self):
        " remove accents from characters "
        self.names = (unidecode(i) for i in self.names)
        return self

    def sub(self, pattern, repl, count=0, flags=0):
        " replace characters that match regular expression "
        regex = re.compile(pattern, flags=flags)
        self.names = [regex.sub(repl, i, count=count)
                      for i in self.names]
        return self

    def replace(self, old, new, count=-1):
        " replace characters that match string "
        self.names = [i.replace(old, new, count) for i in self.names]
        return self

    def whitespace(self, repl):
        " replace whitespace "
        self.names = self.sub(self.WHITESPACE, repl).names
        return self

    def nonalphanums(self, repl):
        " replace non-alphanumeric charaters "
        self.names = self.sub(self.NONALPHANUM, repl).names
        return self

    def numdups(self, fmt='{name}-{number}'):
        " enumerate duplicate names"
        #import pdb; pdb.set_trace()
        duplicate = {k: v for k, v in Counter(self.names).items() if v > 1}
        for name, count in duplicate.items():
            for num in range(1, count + 1):
                idx = self.names.index(name)
                self.names[idx] = fmt.format(name=name, number=num)
        return self

    def as_dict(self):
        " map slugs to original names {slug-name: orig-name, ...} "
        return dict(zip(self.names, self.orig_names))


def slugify(names):
    slugs = Slugs(names).deaccent().trim().lowercase().whitespace('_')
    return slugs.nonalphanums('').numdups().as_dict()
