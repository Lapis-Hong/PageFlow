#!/usr/bin/env python
# coding: utf-8
# @Author: lapis-hong
# @Date  : 2019/5/19
from __future__ import unicode_literals

import requests
import cchardet

from pageflow.cx_extractor import CxExtractor
from pageflow.base import USER_AGENT

test_urls = [
    "https://www.runoob.com/python/python-intro.html",
    "https://news.163.com/19/0519/08/EFHBDI0I00018AP1.html",
]

headers = {'User-Agent': USER_AGENT}

for url in test_urls:
    response = requests.get(url, headers=headers)
    content = response.content
    charset = cchardet.detect(content)
    content = content.decode(charset['encoding'])

    if content:
        text = CxExtractor(100).get_text(content)
        print(text)