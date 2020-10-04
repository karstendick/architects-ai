#!/usr/bin/env python

from setuptools import setup

setup(name='architectsai',
      version='0.0.1',
      description='',
      author='Joshua Karstendick',
      url='http://karstendick.com',
      classifiers=['Programming Language :: Python :: 3 :: Only'],
      py_modules=['architectsai'],
      install_requires=[
          'nose',
          'numpy',
      ],
      entry_points='''
          [console_scripts]
          architectsai=architectsai:main
      ''',
      packages=['architectsai'],
)
