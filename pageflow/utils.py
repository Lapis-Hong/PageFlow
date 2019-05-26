#!/usr/bin/env python
# coding: utf-8
# @Author: lapis-hong
# @Date  : 2019/5/22
"""This module contains some utility functions."""
from __future__ import unicode_literals

from pageflow import LOGGER
from pageflow.result import SearchResult
from pageflow._compat import string_types


def save(result_obj, outfile):
    """Save extract result to file.
    Args:
        result_obj: A list of String or a generator.
        outfile: String, local file path.
    """
    # Turn generator to list.
    result_obj = list(result_obj)
    try:
        with open(outfile, "w") as f:
            for result in result_obj:
                if isinstance(result_obj, string_types):
                    f.write(result + "\n")
                elif isinstance(SearchResult):
                    # TODO
                    f.write(result.url + "\n")
    except IOError as e:
        LOGGER.error("IOError.")


def dump(filename):
    pass