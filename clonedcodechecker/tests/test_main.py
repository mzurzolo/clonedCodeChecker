import unittest
import pytest
import os
import clonedcodechecker as CCC

print(dir())
print(dir(CCC))
ccc = CCC.codechecker.ClonedCodeChecker()
ccc_codecache = CCC.CodeCache()

def test_imports():
    assert all([isinstance(ccc, CCC.ClonedCodeChecker),
                isinstance(ccc_codecache, CCC.CodeCache)])

def test_paths():
    assert all([ccc.output_location == os.path.join(
        os.getcwd(),
        "report.txt"),
                ccc.filecache_location == os.path.join(
                    os.path.expanduser("~"),
                    ".filecache")])
