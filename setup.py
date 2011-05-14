#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
      name='dominion',
      version=__import__('dominion').__version__,
      author='Paul Watts',
      author_email='paulcwatts@gmail.com',
      description='Easy, Pythonic configuration management. Think Puppet for Python/Django. In development',
      license='BSD',
      url='https://github.com/paulcwatts/dominion',
      packages=find_packages()
      )
