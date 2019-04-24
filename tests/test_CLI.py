import unittest
import pytest
import clonedcodechecker as CCC

def test_dr_flags():
    CCC.codechecker.main(['-d', '../opencv'])
    CCC.codechecker.main(['-r', '-d', '../opencv'])
    CCC.codechecker.main(['-r', '-d', '../opencv'])

def test_purge():
    CCC.codechecker.main(['-p'])
