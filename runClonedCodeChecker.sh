#!/bin/sh

PROGRAM="Cloned Code Checker"
VERSION=0.0.1

mkdir -p ./.filecache

./clonedcodechecker/clonedCodeChecker.py "$@"
