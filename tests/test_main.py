import unittest
import pytest
import os
import clonedcodechecker as CCC

def test_imports():
    CCC.codechecker.main(['-tpr'])
