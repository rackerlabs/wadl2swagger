#!/usr/bin/env python

from distutils.core import setup
from setuptools import setup

setup(name='wadl2swagger',
      version='0.0.3',
      description='Convert WADL to Swagger',
      author='Max Lincoln',
      author_email='mlincoln@thoughtworks.com',
      url='http://github.com/rackerlabs/wadl2swagger',
      packages=['wadltools', 'wadltools.cli'],
      entry_points= {'console_scripts':
        [
          'wadl2swagger = wadltools.cli.wadl2swagger:main',
          'wadlcrawler = wadltools.cli.wadlcrawler:main',
        ]
      },
      # can't use ~= operator?
      install_requires = ['wadllib>=1.3', 'pyyaml>=3.0', 'mechanize>=0.2']
)
