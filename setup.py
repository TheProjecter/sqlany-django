#!/usr/bin/env python
# ***************************************************************************
# Copyright (c) 2013 SAP AG or an SAP affiliate company. All rights reserved.
# ***************************************************************************

r"""sqlany-django - SQL Anywhere driver for Django.

http://code.google.com/p/sqlany-django/

----------------------------------------------------------------"""

from setuptools import setup, find_packages

setup(name='sqlany_django',
      version='1.4',
      description='SQL Anywhere database backend for Django',
      long_description=open('README.rst').read(),
      author='Graeme Perrow',
      author_email='graeme.perrow@sap.com',
      url='http://code.google.com/p/sqlany-django',
      packages = find_packages(),
      license='New BSD',
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Framework :: Django',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.4',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Database',
        'Topic :: Software Development :: Libraries :: Python Modules'
        ]
      )
