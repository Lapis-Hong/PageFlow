#!/usr/bin/env python
# coding: utf-8
# @Author: lapis-hong
# @Date  : 2019/5/8
"""This module contains Baidu extractor class."""
from __future__ import unicode_literals

from scrapy.selector import Selector

from pageflow.base import BaseExtractor
from pageflow.result import SearchResult
from pageflow.cx_extractor import CxExtractor

# from pageflow import LOGGER


class Baidu(BaseExtractor):
    """Baidu search results extractor."""

    def __init__(self, proxies=None):
        super(Baidu, self).__init__(proxies)

    def _parse(self, content, **kwargs):
        title, url, abstract, html, content_ = None, None, None, None, None
        if not kwargs:
            kwargs = ["title", "url", "abstract", "html", "content"]
        else:
            kwargs = kwargs.keys()

        result_node_list = Selector(text=content).xpath(
            '//div[contains(@class, "result c-container ") or contains(@class, "result-op c-container xpath-log")]').getall()
        for result_node in result_node_list:
            selector = Selector(text=result_node.replace("<em>", "").replace("</em>", ""))  # Remove <em> </em> tags.
            if "title" in kwargs:
                title = selector.xpath('//h3[contains(@class, "t")]/a/text()').get()
            if "url" in kwargs:
                url = selector.xpath('//h3[contains(@class, "t")]/a/@href').get()
            if "abstract" in kwargs:
                abstract = selector.xpath('//div[contains(@class, "c-span18 c-span-last")]/p/text()').get() \
                    or selector.xpath('//div[contains(@class, "c-abstract")]/text()').get()
                abstract = abstract.strip() if abstract else abstract
            if "html" in kwargs:
                url = selector.xpath('//h3[contains(@class, "t")]/a/@href').get()
                html = self._download(url)
            if "content_" in kwargs:
                content_ = CxExtractor().get_text(html) if html else None
            yield SearchResult(title=title, url=url, abstract=abstract, html=html, content=content_)


