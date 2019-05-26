#!/usr/bin/env python
# coding: utf-8
# @Author: lapis-hong
# @Date  : 2019/5/8
"""This module contains Google extractor class."""
from __future__ import absolute_import

import os
import random


from pageflow._compat import quote_plus, urlparse, parse_qs

# from pageflow import LOGGER
from pageflow.base import BaseExtractor


class Google(BaseExtractor):
    """Google search result Extractor"""

    def filter_link(self, link):
        """
        Returns None if the link doesn't yield a valid result.
        Token from https://github.com/MarioVilas/google
        :return: a valid result
        """
        try:
            # Valid results are absolute URLs not pointing to a Google domain
            # like images.google.com or googleusercontent.com
            o = urlparse(link, 'http')
            if o.netloc:
                return link
            # Decode hidden URLs.
            if link.startswith('/url?'):
                link = parse_qs(o.query)['q'][0]
                # Valid results are absolute URLs not pointing to a Google domain
                # like images.google.com or googleusercontent.com
                o = urlparse(link, 'http')
                if o.netloc:
                    return link
        # Otherwise, or on error, return None.
        except Exception as e:
            LOGGER.exception(e)
            return None

    @staticmethod
    def get_random_domain():
        """Get a random domain.
        Returns:
            Random domain string for google search
        """
        domains_file = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 'data', 'google_domains.txt')
        domains = (line.strip() for line in open(domains_file))
        return random.choice(domains)

