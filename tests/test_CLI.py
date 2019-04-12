import unittest
import pytest
import clonedcodechecker as CCC

def test_t_flag():
    CCC.codechecker.main(['-t'])

def test_dr_flags():
    CCC.codechecker.main(['-d', '/home/travis/'])
    CCC.codechecker.main(['-r', '-d', '/home/travis/'])
    CCC.codechecker.main(['-r', '-d', '/home/travis/'])

def test_purge():
    CCC.codechecker.main(['-p'])
