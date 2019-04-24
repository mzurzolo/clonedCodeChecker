import unittest
import pytest
import os
import clonedcodechecker as CCC

def test_dr_flags():
    CCC.codechecker.main(['-d', '../opencv'])
    CCC.codechecker.main(['-r', '-d', '../opencv'])
    CCC.codechecker.main(['-r', '-d', '../opencv'])
    for fname in os.listdir('../opencv'):
        with open('../opencv/' + fname, 'a') as file:
            print('1', file=file)
    CCC.codechecker.main(['-r', '-d', '../opencv'])

def test_purge():
    CCC.codechecker.main(['-p'])
