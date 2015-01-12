""" SPREADSHEET-STYLE COLUMN ALPHA ID HEADERS
"""

MAX_ALPHA_IDS = 676

def id2num(s):
    """ spreadsheet column name to number
    ref: http://stackoverflow.com/questions/7261936

   :param s: str -- spreadsheet column alpha ID (i.e. A, B, ... AA, AB,...)
   :returns: int -- spreadsheet column number (zero-based index)

    >>> id2num('A')
    0
    >>> id2num('B')
    1
    >>> id2num('XFD')
    16383
    >>>

    """
    n = 0
    for ch in s.upper():
        n = n * 26 + (ord(ch) - 65) + 1
    return n - 1


def num2id(n):
    """
    ref: http://stackoverflow.com/questions/181596

   :param n: int -- spreadsheet column number (zero-based index)
   :returns: int -- spreadsheet column alpha ID (i.e. A, B, ... AA, AB,...)

    >>> num2id(0)
    'A'
    >>> num2id(1)
    'B'
    >>> num2id(16383)
    'XFD'

    """
    s = ''
    d = n + 1
    while d:
        m = (d - 1) % 26
        s = chr(65 + m) + s
        d = int((d - m) / 26)
    return s


def get_ids(num_ids):
    return {i: num2id(i) for i in range(num_ids)}


def add_alphaids(allow_alphaids):
    num_ids = 0
    if self.allow_alphaids:
        try:
            num_ids = int(allow_alphaids)
        except (TypeError, ValueError):
            num_ids = MAX_ALPHA_IDS
    return {i: num2id(i + 1) for i in range(num_ids)}
