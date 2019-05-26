#!/usr/bin/env python
# coding: utf-8
# @Author: lapis-hong
# @Date  : 2019/5/8
import unittest

from pageflow import Baidu


class TestBaidu(unittest.TestCase):
    """
    Test Google class
    """

    def setUp(self):
        self.mg = Baidu()

    def tearDown(self):
        self.mg = None

    def test_get_url(self):
        result = list(self.mg.get_url(query='python'))
        self.assertEqual(result[0], 'https://www.python.org/', 'test get_url fail.')


if __name__ == '__main__':
    unittest.main()

