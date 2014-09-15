import sys

STRING_TYPES = (str, basestring) if sys.version_info.major < 3 else (str,)
