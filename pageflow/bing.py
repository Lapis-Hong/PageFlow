#!/usr/bin/env python
# coding: utf-8
# @Author: lapis-hong
# @Date  : 2019/5/8
"""This module contains Bing extractor class."""
from __future__ import unicode_literals

from scrapy.selector import Selector

from pageflow.base import BaseExtractor
from pageflow.result import SearchResult
from pageflow.cx_extractor import CxExtractor

# from pageflow import LOGGER
from _compat import unquote


class Bing(BaseExtractor):
    """Bing search results Extractor."""

    def __init__(self, proxies=None):
        super(Bing, self).__init__(proxies)

    def _parse(self, content):
        result_node_list = Selector(text=content).xpath(
            '//div[contains(@class, "result c-container ") or contains(@class, "result-op c-container xpath-log")]').getall()
        for result_node in result_node_list:
            result = SearchResult()
            # Remove <em> </em> tags.
            selector = Selector(text=result_node.replace("<em>", "").replace("</em>", ""))
            title = selector.xpath('//h3[contains(@class, "t")]/a/text()').get()
            url = selector.xpath('//h3[contains(@class, "t")]/a/@href').get()

            abstract = selector.xpath('//div[contains(@class, "c-span18 c-span-last")]/p/text()').get() \
                or selector.xpath('//div[contains(@class, "c-abstract")]/text()').get()
            abstract = abstract.strip() if abstract else abstract

            html = self._download(url)
            content = CxExtractor().get_text(html)
            yield SearchResult(title=title, url=url, abstract=abstract, html=html, content=content)


if __name__ == '__main__':

    urls = Bing().get_url("牛肉")
    for url in urls:
        print(url)
    htmls = Bing().get_html("牛肉")
    # for html in htmls:
    #     print(html)
    result = Bing().get("牛肉")
    print(result.next())
