import unittest
import pytest
import os
import clonedcodechecker as CCC

def test_dr_flags():
    os.sys("ccc -d ../opencv")
    os.sys("ccc -rd ../opencv")
    os.sys("ccc -rjd ../opencv")
    os.sys("ccc -rd ../opencv")
    for fname in os.listdir('../opencv'):
        try:
            with open('../opencv/' + fname, 'a') as file:
                print('1dddddd', file=file)
        except:
            continue
    os.sys("ccc -rd ../opencv")

def test_purge():
    os.sys("ccc -p")
