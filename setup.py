#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os

from setuptools import find_packages, setup

# Package meta-data.
NAME = 'fakemenot'
DESCRIPTION = 'A simple python package to check if a Tweet is genuine or not.'
URL = 'https://github.com/sachinkamath/fakemenot'
EMAIL = 'Sachin S Kamath'
AUTHOR = 'me@sachinwrites.xyz'

# What packages are required for this module to be executed?
REQUIRED = [
    'pytesseract',
    'twittersearch',
    'termcolor',
    'Pillow',
]

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# This will only work if 'README.rst' is present in your MANIFEST.in file!
with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = '\n' + f.read()

# Where the magic happens:
setup(
    name=NAME,
    version='0.0.3',
    description=DESCRIPTION,
    entry_points={
        'console_scripts': [
            'fakemenot = fakemenot.main:main',
        ],
    },
    long_description=long_description,
    author=AUTHOR,
    author_email=EMAIL,
    keywords='twitter fake tweets',
    url=URL,
    packages=find_packages(exclude=('tests',)),
    install_requires=REQUIRED,
    include_package_data=True,
    license='MIT',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
    ],
)
