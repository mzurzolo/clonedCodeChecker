#!/usr/bin/env python3

from datetime import datetime
import setuptools


def main():
    now = datetime.now()
    now_midnight = datetime(year=now.year,
                            month=now.month,
                            day=now.day
                            ).timestamp()

    setuptools.setup(name='clonedcodechecker',
          version='0.0.1.{}'.format(now_midnight),
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
          install_requires=['ruamel.yaml'],
          entry_points={
              'console_scripts': [
                  'ccc = clonedcodechecker.codechecker:run'
              ]
          })


if __name__ == '__main__':
    main()
