#!/usr/bin/env python
# coding: utf-8
# @Author: lapis-hong
# @Date  : 2019/5/8
import re
from setuptools import find_packages, setup


def find_version(fname):
    """Attempts to find the version number in the file fname.
    Raises RuntimeError if not found.
    """
    version = ''
    with open(fname, 'r') as fp:
        reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
        for line in fp:
            m = reg.match(line)
            if m:
                version = m.group(1)
                break
    if not version:
        raise RuntimeError('Cannot find version information')
    return version


__version__ = find_version('pageflow/__init__.py')


setup(
    name='pageflow',
    version=__version__,
    author="Lapis-Hong",
    author_email="dhq1125@163.com",
    url="https://github.com/lapis-hong/PageFlow",
    license="MIT",
    keywords=["pageflow", "search result spider", "web information extraction"],
    description="Simple, powerful and pythonic web page search results crawler.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    install_requires=["requests>=2.12", "scrapy>=1.6.0", "cchardet"],
    packages=find_packages(exclude=("test*", )),
    package_data={"data": ["*.txt"]},
    classifiers=(
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        "Topic :: Text Processing",
    )
)
