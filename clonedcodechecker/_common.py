#!/usr/bin/env python3

import os

# filenames made from the absolute path of the file will be unique
def cacheFileName(path):
    if path != abspath(path):
        path = abspath(path)
    # remove the first /, replace slashes with dots, add file extension
    # this: [1:] means "from the first element to the end."
    # list[1:10] would give me from the first element to the 9th
    # list[1:-1] would give me everything but the first and last element
    return path.replace("/", ".")[1:] + ".yaml"

def abspath(filename):
    return os.path.abspath(filename)

# this is where the filter is defined in that ugly list(filter(map(lambda))) line
# in cppFile.py.
def fun(item):
    # empty lines get filtered
    if len(item) == 0:
        return False
    # the middle of block comments
    if item[0] == "*":
        return False
    # the first line of a block commment
    if item[0:1] == "/*":
        return False
    
    return True
