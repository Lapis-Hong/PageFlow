#!/usr/bin/env python
# coding: utf-8
# @Author: lapis-hong
# @Date  : 2019/5/19
"""This module contains class `pageflow.pages.PageUrlGenerator`."""
from __future__ import unicode_literals

from _compat import quote_plus, urlencode

# TODO: more args
SEARCH_ENGINES = {
    'google': 'https://www.google/com/search?q={query}&start={num}',
     # 'bing': 'https://cn.bing.com/?FORM=BEHPTB',
    'bing': 'https://www.bing.com/search?q={query}&first={num}',
    'baidu': 'https://www.baidu.com/s?wd={query}&pn={num}'
}


class PageUrlGenerator(object):
    """Generate search page url given total page numbers."""

    def __init__(self, query, search_engine, total_page=1):
        if isinstance(query, unicode):
            query = str(query)
        # self.query = quote(query)
        self.query = quote_plus(query)
        self.search_engine = search_engine.lower()
        self.search_engine_url = SEARCH_ENGINES[self.search_engine]
        self.current_page = 0
        self.total_page = total_page

    def _current_url(self):
        return self.search_engine_url.format(query=self.query, num=str(self.current_page * 10))

    def __iter__(self):
        return self

    def next(self):
        if self.current_page < self.total_page:
            url = self._current_url()
            self.current_page += 1
            return url
        raise StopIteration
