import unittest
import pytest
import os
import clonedcodechecker as CCC

def test_coverage():
    CCC.codechecker.main(['-pr'])

def test_imports():
    ccc = CCC.codechecker.ClonedCodeChecker()
    ccc_codecache = CCC.codecache.CodeCache()
    assert all([isinstance(ccc, CCC.codechecker.ClonedCodeChecker),
                isinstance(ccc_codecache, CCC.codecache.CodeCache)])


def test_matcher():
    tester = CCC.matcher.Matcher()
    assert tester.tok_regex['FIRST_FILTER'].find("//testing\n").lastgroup == 'DOUBLE_SLASH_COMMENT'
