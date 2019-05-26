#!/usr/bin/env python
# coding: utf-8
# @Author: lapis-hong
# @Date  : 2019/5/8
"""Compatibility for python2 and python3."""
from __future__ import unicode_literals

import sys

# try:
#     import cPickle as pickle
# except ImportError:
#     import pickle

# PY2 = int(sys.version[0]) == 2
PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

if PY2:
    import cPickle as pickle
    from itertools import imap, izip
    from urllib import quote, unquote, urlencode, quote_plus
    from urlparse import urlparse, parse_qs

    reload(sys)
    sys.setdefaultencoding('utf8')

    text_type = unicode
    binary_type = str
    string_types = (str, unicode)
    unicode = unicode
    basestring = basestring
    imap = imap
    izip = izip

# PY3
else:
    import pickle
    from urllib.parse import quote, unquote, quote_plus, urlencode, urlparse, parse_qs

    text_type = str
    binary_type = bytes
    string_types = (str,)
    unicode = str
    basestring = (str, bytes)
    imap = map
    izip = zip







