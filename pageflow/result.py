#!/usr/bin/env python
# coding: utf-8
# @Author: lapis-hong
# @Date  : 2019/5/19
"""This module contains the definition of result class `pageflow.result.SearchResult`."""
from __future__ import unicode_literals


class SearchResult(object):
    """SearchResult class contains 5 members {`title`, `abstract`, `url`, `html`, `content`} 
    (which can be access by instance.member) and 1 method `set`.
    
    Usage:
    >>> result = SearchResult()
    >>> print(result)
    >>> result.title
    "python"
    >>> result.set(title="Python")
    >>> result.title
    "Python"
    """
    def __init__(self, title=None, abstract=None, url=None, html=None, content=None):
        self._title = title
        self._abstract = abstract
        self._url = url
        self._html = html
        self._content = content

    def set(self, title=None, abstract=None, url=None, html=None, content=None):
        self._title = title
        self._abstract = abstract
        self._url = url
        self._html = html
        self._content = content

    @property
    def title(self):
        return self._title

    @property
    def abstract(self):
        return self._abstract

    @property
    def url(self):
        return self._url

    @property
    def html(self):
        return self._html

    @property
    def content(self):
        return self._content

    def __str__(self):
        """Return a string containing a nicely printable representation of an object.
        >>> result = SearchResult()
        >>> print(result)
        """
        return "{:<10}{}\n{:<10}{}\n{:<10}{}\n{:<10}{}\n{:<10}{}".format(
            "title:", self._title, "abstract", self._abstract, "url:", self._url,
            "content:", self._content.replace("\n", r"\n") if self._content else None,
            "html:", "Too long to display." if self._html else None)

    def __repr__(self):
        """Overwrite __str__ method to control the printable representation of an object
        >>> result = SearchResult()
        >>> result
        <pageflow.result.SearchResult at 0x111e2a8d0>  # default representation
        SearchResult(title=None, abstract=None, url=None, content=None, html=None)  # new representation 
        """
        return "{self.__class__.__name__}(title={self._title}, abstract={self._abstract}," \
               " url={self._url}, content={self._content}, html={self._html})".format(self=self)

    # __repr__ = __str__




