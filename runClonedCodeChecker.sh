#!/bin/sh

PROGRAM="Cloned Code Checker"
VERSION=0.0.1

mkdir -p .$CCC_ENV/.filecache

$CCC_ENV/clonedcodechecker-mercurial/clonedcodechecker/clonedCodeChecker.py -e $CCC_ENV "$@"
