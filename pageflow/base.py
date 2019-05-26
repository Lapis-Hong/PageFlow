#!/usr/bin/env python
# coding: utf-8
# @Author: lapis-hong
# @Date  : 2019/5/8
"""Abstract base class for all search engine extractor descendant classes."""
from __future__ import absolute_import
from __future__ import unicode_literals

import os
import time
import random
import logging
from abc import ABCMeta, abstractmethod
from six import with_metaclass

import requests
import cchardet
from scrapy.selector import Selector

# from pageflow import LOGGER
from pageflow.pages import PageUrlGenerator


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s: %(message)s')
LOGGER = logging.getLogger('PageFlow')

USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) ' \
             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'

# Search result urls xpath for different search engine.
SEARCH_URLS_XPATH = {
    'google': '//h3/a/@href',
    'bing': '//h2/a/@href',
    'baidu': '//h3/a/@href',
}


class BaseExtractor(with_metaclass(ABCMeta)):
    """Abstract base extractor class for all extractor sub-classes.
    Descendant classes must implement abstract method `_parse`.
    Each extractor class can get 5 types of information from the web pages.
    This class defines all the interface methods. Including
        `get_html`             --Get all search pages html content;
        `get_url`              --Get all search result pages urls;
        `get_title`            --Get all search result titles;
        `get_abstract`         --Get all search result abstract;
        `get_redirect_html`    --Get all search result redirect pages html;
        `get_redirect_content` --Get all search result redirect pages content;
        `get`                  --Get all search result titles, abstract, urls;
        `get_all`              --Get everything.
    """
    def __init__(self, proxies=None):
        self.proxies = random.choice(proxies) if proxies else None
        self.search_engine = self.__class__.__name__.lower()
        self.url_xpath = SEARCH_URLS_XPATH[self.search_engine]

    def get_html(self, query, pages=1, **kwargs):
        """Get all search pages html content.
        Args:
            query: String, search query string.
            pages: Int, search pages number, defaults to 1.
            kwargs: Other keywords arguments.
        Returns:
            A generator for search pages html content.
        """
        return self._search_pages_html_generator(query, pages, **kwargs)

    def get_url(self, query, pages=1, **kwargs):
        """Get all search result pages urls.
        Args: 
            query: String, search query string.
            pages: Int, search pages number, defaults to 1.
            **kwargs: Other keywords arguments.
        Returns:
            A generator for search result pages urls.
        """
        # for content in self._search_pages_html_generator(query, pages, **kwargs):
        #     result_urls = self._parse_urls(content)
        #     for url in result_urls:
        #         yield url
        for content in self.get_html(query, pages, **kwargs):
            results = self._parse(content, url=True)
            for result in results:
                yield result

    def get_title(self, query, pages=1, **kwargs):
        """Get all search result titles.
        Args: 
            query: String, search query string.
            pages: Int, search pages number, defaults to 1.
            **kwargs: Other keywords arguments.
        Returns:
            A generator for search result titles
        """
        for content in self.get_html(query, pages, **kwargs):
            results = self._parse(content, title=True)
            for result in results:
                yield result

    def get_abstract(self, query, pages=1, **kwargs):
        """Get all search result abstract (
        the result summary which is appeared in the origin search page).
        Args: 
            query: String, search query string.
            pages: Int, search pages number, defaults to 1.
            **kwargs: Other keywords arguments.
        Returns:
            A generator for search result abstract.
        """
        for content in self.get_html(query, pages, **kwargs):
            results = self._parse(content, abstract=True)
            for result in results:
                yield result

    def get_redirect_html(self, query, pages=1, **kwargs):
        """Get all search result redirect pages html.
        Args: 
            query: String, search query string.
            pages: Int, search pages number, defaults to 1.
            **kwargs: Other keywords arguments.
        Returns:
            A generator for search result redirect html.
        """
        for content in self.get_html(query, pages, **kwargs):
            results = self._parse(content, html=True)
            for result in results:
                yield result

    def get_redirect_content(self, query, pages=1, **kwargs):
        """Get all search result redirect pages content (base on CX-extractor).
        Args: 
            query: String, search query string.
            pages: Int, search pages number, defaults to 1.
            **kwargs: Other keywords arguments.
        Returns:
            A generator for search result redirect content.
        """
        for content in self.get_html(query, pages, **kwargs):
            results = self._parse(content, content_=True)
            for result in results:
                yield result

    def get(self, query, pages=1, **kwargs):
        """Get everything.
        Args: 
            query: String, search query string.
            pages: Int, search pages number, defaults to 1.
            **kwargs: other key words arguments 
        Returns:
            A generator of SearchResult object.
        """
        for content in self.get_html(query, pages, **kwargs):
            results = self._parse(content, title=True, url=True, abstract=True)
            for result in results:
                yield result

    def get_all(self, query, pages=1, **kwargs):
        """Get everything.
        Args: 
            query: String, search query string.
            pages: Int, search pages number, defaults to 1.
            **kwargs: other key words arguments 
        Returns:
            A generator of SearchResult object.
        """
        for content in self.get_html(query, pages, **kwargs):
            results = self._parse(content)
            for result in results:
                yield result

    def _search_pages_html_generator(self, query, pages=1, **kwargs):
        """Search pages html content generator.
        Args:
            query: String, search query string.
            pages: Int, search pages number, defaults to 1.
            kwargs: Other keywords arguments.
        Returns:
            A generator for search pages html content.
        """
        page_urls = PageUrlGenerator(query, self.search_engine, pages)
        for page_url in page_urls:
            yield self._download(page_url)

    def _download(self, url, user_agent=None, retry=3, delay=2):
        """Html content downloader.
        Args:
            url: String, url string.
            user_agent: String, user agent string.
            retry: Int, request retry times.
            delay: Int, random delay upper bound.
        Returns:
            Html content or None if not succeed.
        """
        content = None
        user_agent = user_agent or USER_AGENT
        # Add headers
        headers = {'User-Agent': user_agent}
        requests.packages.urllib3.disable_warnings()
        while retry > 0:
            try:
                response = requests.get(
                    url=url,
                    proxies=self.proxies,
                    headers=headers,
                    allow_redirects=True,  # fix 302
                    verify=False,  # avoid ssl certification
                    timeout=10)
                if response.status_code != 200:
                    print(response.status_code)
                    self._random_sleep(upper=delay)
                    retry -= 1
                    continue
                content = response.content
                charset = cchardet.detect(content)
                content = content.decode(charset['encoding'])
                break

            except requests.exceptions as e:
                LOGGER.exception(e)
                print(e)
                self._random_sleep(upper=delay)
                retry -= 1
                continue

        return content

    @abstractmethod
    def _parse(self, content, **kwargs):
        """Abstract method, must be implemented in sub-classes.
        Args:
            content: String, html content stirng.
            **kwargs: other key words arguments, if we pass title=True into
            it, then it only parse title part.
        Returns:
            Search Result object contains extraction info.
        """
        return

    def _parse_urls(self, content):
        """Parse search page result urls.
        Args:
            content: String, html content.
        Returns:
            List of urls.
        """
        return Selector(text=content).xpath(self.url_xpath).getall()

    @staticmethod
    def _get_random_user_agent():
        """Get a random user agent string from `data/user_agents.txt`."""
        user_agents_file = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 'data', 'user_agents.txt')
        user_agents = (line.strip() for line in open(user_agents_file))
        return random.choice(user_agents)

    @staticmethod
    def _random_sleep(lower=0, upper=3):
        """Random sleep.
        Args:
            lower: Int, lower random bound.
            upper: Int, upper random bound.
        """
        sleep_time = random.randint(lower, upper)
        time.sleep(sleep_time)






