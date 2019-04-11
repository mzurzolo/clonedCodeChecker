import unittest
import pytest
import clonedcodechecker as CCC

def test_purge():
    CCC.codechecker.main(['-p'])

def test_recursive():
    CCC.codechecker.main(['-r'])

def test_d_flag():
    CCC.codechecker.main(['-d ../'])


def test_help():
    CCC.codechecker.main(['-h'])

def test_t_flag():
    CCC.codechecker.main(['-t'])
