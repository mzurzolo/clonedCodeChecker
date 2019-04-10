#!/usr/bin/env python3

from setuptools import setup,find_packages
from setuptools import wheel

setup(name='clonedcodechecker',
      version='0.0.1',
      description='Cloned C++ Code Checker',
      url='https://sourceforge.net/p/clonedcodechecker/mercurial/ci/default/tree/',
      author='Michael Zurzolo <mikezurzolo@gmail.com>,\
              Michael Turner <mt9u14@gmail.com>,\
              Tajhay Felder <felder62@students.rowan.edu>,\
              Kevin Eivich <eivichk6@students.rowan.edu>,\
              Dylan Anderson <dylanjanderson4@gmail.com>,\
              Emily Fliegel <fliege39@students.rowan.edu>',
      author_email='listed in author',
      license='BSD-3',
      packages=find_packages(),
      install_requires=['ruamel.yaml'],
      entry_points={
          'console_scripts': [
              'ccc = clonedcodechecker.clonedcodechecker:__main__'
          ]
      },
      include_package_data=True)
