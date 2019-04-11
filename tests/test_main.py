import unittest
import pytest
import os
import clonedcodechecker as CCC

def test_coverage():
    CCC.codechecker.main(['-tpr'])

def test_imports():
    ccc = CCC.codechecker.ClonedCodeChecker()
    ccc_codecache = CCC.codecache.CodeCache()
    assert all([isinstance(ccc, CCC.codechecker.ClonedCodeChecker),
                isinstance(ccc_codecache, CCC.codecache.CodeCache)])
