#!/bin/sh

PROGRAM="Cloned Code Checker"
VERSION=0.0.1

mkdir -p $CCC_ENV/.filecache

$CCC_ENV/py37/bin/python3 $CCC_ENV/clonedcodechecker/\
clonedCodeChecker.py -e $CCC_ENV -o $(pwd)/report.txt "$@"
