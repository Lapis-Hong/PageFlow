#!/usr/bin/env python
# coding: utf-8
# @Author: lapis-hong
# @Date  : 2019/5/8
"""PageFlow is a python package for extracting search result from web pages."""
from __future__ import unicode_literals

# import os
import logging

from .google import Google
from .baidu import Baidu
from .bing import Bing


__version__ = '0.1'
__license__ = 'MIT'
__author__ = 'Lapis-Hong'

__all__ = [
    'Google',
    'Baidu',
    'Bing',
    'PageFlow'
]

# PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))


class PageFlow(object):
    """Wrapper class for Google, Baidu and Bing class."""
    def __new__(cls, search_engine, *args, **kwargs):
        cls.se = search_engine.lower()
        if cls.se == "google":
            return Google(*args, **kwargs)
        elif cls.se == "baidu":
            return Baidu(*args, **kwargs)
        elif cls.se == "bing":
            return Bing(*args, **kwargs)
        else:
            raise ValueError(
                "Search engine must be one of `google`, `baidu` or `bing`, found `{}`".format(cls.se))




