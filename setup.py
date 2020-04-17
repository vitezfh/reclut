#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

from setuptools import setup, find_packages

import reclut

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='reclut',
    version=reclut.__version__,
    packages=find_packages(),
    author='vitezfh',
    author_email='vitezfh@gmail.com',
    description='Download media from subreddits - and other tools',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'requests',
        'youtube_dl',
        "praw"
    ],
    url='https://github.com/vitezfh/reclut',
    classifiers=[
        'Programming Language :: Python',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Topic :: Internet',
        'Topic :: Multimedia :: Sound/Audio',
    ],
    entry_points={
        'console_scripts': [
            'reclut = reclut.reclut:main',
        ],
    },
)
