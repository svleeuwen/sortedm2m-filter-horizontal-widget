#!/usr/bin/env python
# -*- coding: utf-8 -*-
import codecs
import os
import re
import sys
from setuptools import setup


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


def read(*parts):
    return codecs.open(os.path.join(os.path.dirname(__file__), *parts),
                       encoding='utf8').read()


try:
    bytes
except NameError:
    bytes = str


long_description = '\n\n'.join((
    read('README.rst'),
    read('CHANGES.rst'),
))

version = find_version('sortedm2m_filter_horizontal_widget', '__init__.py')

setup(
    name = 'django-sortedm2m-filter-horizontal-widget',
    version = version,
    url = 'https://github.com/svleeuwen/sortedm2m-filter-horizontal-widget',
    download_url = 'https://github.com/svleeuwen/sortedm2m-filter-horizontal-widget/archive/{}.tar.gz'.format(version),
    license = 'BSD',
    description = 'Horizontal filter widget for django-sortedm2m',
    long_description = long_description,
    author = u'Sander van Leeuwen',
    author_email = 'replytosander@gmail.com',
    packages = ['sortedm2m_filter_horizontal_widget'],
    include_package_data = True,
    zip_safe = False,
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    install_requires = ['django-sortedm2m'],
)
