#!/bin/sh

TARGET="$(pwd)"

export PATH=$TARGET/py37/bin:$PATH
export CCC_ENV=$TARGET

if [ ! -d "$TARGET/py37" ] ; then
  python3 -m venv $TARGET/py37
  python3 -m pip install -r $TARGET/requirements.txt
  ln -s -T $TARGET/devClonedCodeChecker.sh $TARGET/py37/bin/ccc
fi
