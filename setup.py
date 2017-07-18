"""A setuptools based setup module for Albatross"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from codecs import open
from os import path
from setuptools import setup, find_packages

import versioneer

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as readme_file:
    readme = readme_file.read()

with open(path.join(here, 'HISTORY.rst'), encoding='utf-8') as history_file:
    history = history_file.read().replace('.. :changelog:', '')

requirements = [
    # TODO: put package requirements here
    'ply',
    'decorator',
    'six',
    'jsonpath-rw>=1.2.0',
    'pbr>=1.8',
    'jsonpath-rw-ext',
    'xlrd',
    'xlwt',
    'requests',
    'xpath-py',
    'mysql-connector'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='Albatross',
    version='1.0.1',
    cmdclass=versioneer.get_cmdclass(),
    description="Python Libraries with Generic (Excel, Shell, SQL, JSON/XML Parsers etc) and Hadoop (Storm,Hbase, Kafka etc ) Essentials!",
    long_description=readme + '\n\n' + history,
    author="DURGASURESH KAGITHA",
    author_email='durgasuresh_kvsd@yahoo.in',
    url='https://github.com/KVSDURGASURESH/ALBATROSS',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    entry_points={
        'console_scripts':[
            'ALBATROSS=Albatross.cli:cli',
            ],
        },
    include_package_data=True,
    install_requires=requirements,
    license="GPL",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Topic :: Education :: Testing',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
        'Topic :: Utilities',
        'Topic :: Database :: Database Engines/Servers'
    ],
    keywords=[
        'python libraries for excel',
        'python libraries for sql',
        'python libraries for shell'
        'python libraries for kafka'
        'python libraries for accessing stormAPI'
        'python libraries for xml and json parsers'
        'python libraries for loggers or logging'
    ],
    test_suite='tests',
    tests_require=test_requirements,
)
