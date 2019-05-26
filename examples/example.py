#!/usr/bin/env python
# coding: utf-8
# @Author: lapis-hong
# @Date  : 2019/5/8
"""A simple example of extracting search result from web pages.
"""
from __future__ import unicode_literals

from pageflow import PageFlow


query = "python"
pages = 1  # search results total pages

# PROXIES = [{
#     'http': 'http://192.168.2.207:1080',
#     'https': 'http://192.168.2.207:1080'
# }]

pf = PageFlow("baidu", proxies=None)

# Get search page html.
html = pf.get_html(query=query, pages=pages)
# print(html.next())

# Get search result urls.
url = pf.get_url(query=query, pages=pages)
# print(url.next())

# Get search result titles.
title = pf.get_title(query=query, pages=pages)
# print(title.next())

# Get search result abstract.
abstract = pf.get_abstract(query=query, pages=pages)
# print(abstract.next())

# Get search result redirect html.
redirect_html = pf.get_redirect_html(query=query, pages=pages)
# print(redirect_html.next())

# Get search result redirect content.
redirect_content = pf.get_redirect_content(query=query, pages=pages)
# print(redirect_content.next())

# Get search result title, abstract and url.
result = pf.get(query=query, pages=pages)
# print(result.next())

# Get search result title, abstract, url, redirect html and redirect content.
result_all = pf.get_all(query=query, pages=pages)
# print(result_all.next())










