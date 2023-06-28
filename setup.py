#!/usr/bin/env python

from setuptools import setup

DEPENDENCIES = open('requirements.txt', 'r').read().split('\n')
README = open('./docs/README_CN.md', 'r').read()


setup(
    name = 'FOFA',
    version = '2.0.1',
    description = 'Python library for FOFA (https://fofa.info)',
    long_description=README,
    long_description_content_type="text/markdown",
    author = 'Fofa',
    author_email = 'fofabot@baimaohui.net',
    url = 'https://github.com/fofapro/fofa-py',
    packages = ['fofa'],
    entry_points={'console_scripts': ['fofa=fofa.__main__:main']},
    install_requires=DEPENDENCIES,
    license = "MIT",
    requires_python=">=3.7",
    keywords=['fofa', 'security', 'network'],
    classifiers = [
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        "Programming Language :: Python :: 3.11",
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
