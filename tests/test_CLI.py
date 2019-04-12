import unittest
import pytest
import clonedcodechecker as CCC

def test_t_flag():
    CCC.codechecker.main(['-t'])

def test_dr_flags():
    CCC.codechecker.main(['-d', '/home/travis/virtualenv'])
    CCC.codechecker.main(['-r', '/home/travis/virtualenv'])
    CCC.codechecker.main(['-r', '-d', '/home/travis/virtualenv'])

def test_purge():
    CCC.codechecker.main(['-p'])
