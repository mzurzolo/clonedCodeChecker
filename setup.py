#!/usr/bin/env python3

from datetime import datetime
import setuptools


def rewrite_init():
    """Version by day timestamp."""
    now = datetime.now()
    now_midnight = int(
        datetime(year=now.year, month=now.month, day=now.day).timestamp()
    )
    with open("clonedcodechecker/__init__.py", "w") as file:
        print('__name__ = "clonedcodechecker"', file=file)
        print('__version__ = "0.0.1.{}"'.format(now_midnight), file=file)
        print("from . import codecache", file=file)
        print("from . import codechecker", file=file)
        print("from . import matcher", file=file)

    return now_midnight


def main():
    """Package"""
    setuptools.setup(
        name="clonedcodechecker",
        version="0.0.1.{}".format(rewrite_init()),
        description="Cloned C++ Code Checker",
        url="https://sourceforge.net/p/clonedcodechecker/mercurial/ci/default/tree/",
        author="Michael Zurzolo <mikezurzolo@gmail.com>,\
                  Michael Turner <mt9u14@gmail.com>,\
                  Tajhay Felder <felder62@students.rowan.edu>,\
                  Kevin Eivich <eivichk6@students.rowan.edu>,\
                  Dylan Anderson <dylanjanderson4@gmail.com>,\
                  Emily Fliegel <fliege39@students.rowan.edu>",
        author_email="listed in author",
        license="BSD-3",
        install_requires=["ruamel.yaml"],
        entry_points={
            "console_scripts": ["ccc = clonedcodechecker.codechecker:main"]
        },
    )


if __name__ == "__main__":
    rewrite_init()
    main()
