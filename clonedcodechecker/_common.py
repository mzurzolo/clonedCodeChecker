#!/usr/bin/env python3

import os


def cacheFileName(path):
    if path != os.path.abspath(path):
        path = os.path.abspath(path)
    # remove the first /, replace slashes with dots, add file extension
    return path.replace("/", ".")[1:] + ".yaml"

def fun(item):
    if len(item) == 0:
        return False
    if item[0] == "*":
        return False
    if item[0:1] == "/*":
        return False
    return True
