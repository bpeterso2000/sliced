import sys

StringType = [str]

if sys.version_info.major < 3:
    StringType.append(unicode)
    range = xrange
