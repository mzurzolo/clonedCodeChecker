#!/bin/sh

TARGET="$(pwd)"

export PATH=$TARGET/py37/bin:$PATH
export CCC_ENV=$TARGET

if [ ! -d "$TARGET/py37" ] ; then
  python3 -m venv $TARGET/py37
  python3 -m pip install -r $TARGET/requirements_dev.txt
  python setup.py install
fi
