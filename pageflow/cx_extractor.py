#!/usr/bin/env python
# coding: utf-8
# @Author: lapis-hong
# @Date  : 2019/5/19
"""This module used to extract main text from arbitrary html content using CX-extractor."""
from __future__ import unicode_literals

import re


class CxExtractor(object):
    """Cx-extractor implemented in Python, 
    based on https://github.com/chrislinan/cx-extractor-python
    """

    def __init__(self, threshold=100, blocks_width=3):
        self._blocks_width = blocks_width
        self._threshold = threshold
        self._text = []
        self._index_distribution = []

    def get_text(self, content):
        content = self._filter_tags(content)
        lines = content.split('\n')
        for i in range(len(lines)):
            lines[i] = re.sub("\r|\n|\\s{2,}", "", lines[i])
        for i in range(0, len(lines) - self._blocks_width):
            words_num = 0
            for j in range(i, i + self._blocks_width):
                lines[j] = lines[j].replace("\\s", "")
                words_num += len(lines[j])
            self._index_distribution.append(words_num)
        start = -1
        end = -1
        boolstart = False
        boolend = False
        if len(self._index_distribution) < 3:
            return 'This page has no content to extract.'
        for i in range(len(self._index_distribution) - 3):
            if self._index_distribution[i] > self._threshold and (not boolstart):
                if self._index_distribution[i + 1] != 0 or self._index_distribution[i + 2] != 0 or self._index_distribution[i + 3] != 0:
                    boolstart = True
                    start = i
                    continue
            if boolstart:
                if self._index_distribution[i] == 0 or self._index_distribution[i + 1] == 0:
                    end = i
                    boolend = True
            tmp = []
            if boolend:
                for ii in range(start, end+1):
                    if len(lines[ii]) < 5:
                        continue
                    tmp.append(lines[ii] + "\n")
                str = "".join(list(tmp))
                if "Copyright" in str or "版权所有" in str:
                    continue
                self._text.append(str)
                boolstart = boolend = False
        result = "".join(self._text)
        if result == '':
            return 'This page has no content to extract.'
        else:
            return result

    def _filter_tags(self, html):
        re_doctype = re.compile('<![DOCTYPE|doctype].*>')
        re_nav = re.compile('<nav.+</nav>')
        re_cdata = re.compile('//<!\[CDATA\[.*//\]\]>', re.DOTALL)
        re_script = re.compile('<\s*script[^>]*>.*?<\s*/\s*script\s*>', re.DOTALL | re.I)
        re_style = re.compile('<\s*style[^>]*>.*?<\s*/\s*style\s*>', re.DOTALL | re.I)
        re_textarea = re.compile('<\s*textarea[^>]*>.*?<\s*/\s*textarea\s*>', re.DOTALL | re.I)
        re_br = re.compile('<br\s*?/?>')
        re_h = re.compile('</?\w+.*?>', re.DOTALL)
        re_comment = re.compile('<!--.*?-->', re.DOTALL)
        re_space = re.compile('r[\t ]+')
        s = re_cdata.sub('', html)
        s = re_doctype.sub('', s)
        s = re_nav.sub('', s)
        s = re_script.sub('', s)
        s = re_style.sub('', s)
        s = re_textarea.sub('', s)
        s = re_br.sub('', s)
        s = re_h.sub('', s)
        s = re_comment.sub('', s)
        s = re_space.sub(' ', s)
        s = self._replace_char_entity(s)
        return s

    def _replace_char_entity(self, html):
        CHAR_ENTITIES = {'nbsp': ' ', '160': ' ',
                         'lt': '<', '60': '<',
                         'gt': '>', '62': '>',
                         'amp': '&', '38': '&',
                         'quot': '"', '34': '"', }
        re_char_entity = re.compile(r'&#?(?P<name>\w+);')
        sz = re_char_entity.search(html)
        while sz:
            entity = sz.group()
            key = sz.group('name')
            try:
                html = re_char_entity.sub(CHAR_ENTITIES[key], html, 1)
                sz = re_char_entity.search(html)
            except KeyError:
                html = re_char_entity.sub('', html, 1)
                sz = re_char_entity.search(html)
        return html

