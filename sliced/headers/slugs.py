import re
import sys
from collections import Counter

from unidecode import unidecode


class Slugs:

    def __init__(self, names):
        self.orig_names = self.names = names
        self.whitespace = re.compile(r'\s+')
        self.nonalphanum = re.compile(r'[^\w_]')

    def trim(self, chars=None):
       self.names = (i.strip(chars) for i in self.names)
       return self

    def lowercase(self):
       self.names = (i.lower() for i in self.names)
       return self

    def deaccent(self):
        self.names = (unidecode(i) for i in self.names)
        return self

    def sub(self, pattern, repl, count=0, flags=0):
        regex = re.copmile(pattern)
        self.names = (regex.sub(repl, i, count=count, flags=flags)
                      for i in self.names)
        return self

    def replace(self, old, new, count=-1):
        self.names = (i.replace(old, new, count) for i in self.names)
        return self

    def whitespace(self, repl):
        return sub(self.whitespace, repl)

    def nonalphanums(self, repl):
        return sub(self.nonalphanum, repl)

    def numdups(self, fmt='{name}{number}'):
        " enumerate duplicate names"
        duplicate = (c for c in Counter(self.names) if c > 1)
        for name, count in duplicate.items():
            for num in range(count, 1):
                idx = self.names.index(name)
                self.names[idx] = fmt.format(name=name, number=num)
        return self

    def as_dict(self):
        " map slugs to original names {slug-name: orig-name, ...} "
        return dict(zip(self.names, self.orig_names))


def slugify(names):
    slugs = Slugs(names)
    slugs = slugs.lowercase().deaccent().whitespace('_').nonalphanums('')
    return slugs.numdups().as_dict()
