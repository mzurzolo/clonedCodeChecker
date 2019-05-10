#!/bin/sh
mv .hgignore .hg/
hg purge
mv .hg/.hgignore ./
rm -fR html
rm -f RELEASES/ccc.latest.tar.gz
mkdir RELEASES/ccc.latest

source scripts/work_here.sh
mvn -f clonedcodecheckerplugin clean package
python3 setup.py sdist bdist bdist_wheel

mv clonedcodecheckerplugin/target/clonedcodechecker-1.0.0-SNAPSHOT.jar RELEASES/ccc.latest/
mv dist/* RELEASES/ccc.latest/

tar -czvf RELEASES/ccc.latest.tar.gz RELEASES/ccc.latest
pdoc --html clonedcodechecker
