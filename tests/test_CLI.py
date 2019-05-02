import unittest
import pytest
import mock
import os
import clonedcodechecker as CCC


def test_dr_flags():

    CCC.codechecker.main(["-d", "../opencv"])
    CCC.codechecker.main(["-r", "-d", "../opencv"])
    CCC.codechecker.main(["-rj", "-d", "../opencv"])
    CCC.codechecker.main(["-r", "-d", "../opencv"])
    for fname in os.listdir("../opencv"):
        try:
            with open("../opencv/" + fname, "a") as file:
                print("1dddddd", file=file)
        except:
            continue
    CCC.codechecker.main(["-r", "-d", "../opencv"])


def test_purge():
    CCC.codechecker.main(["-p"])


# thank you https://medium.com/opsops/how-to-test-if-name-main-1928367290cb
def test_init():
    from clonedcodechecker import codechecker
    with mock.patch.object(codechecker, "main", return_value=42):
        with mock.patch.object(codechecker, "__name__", "__main__"):
            with mock.patch.object(codechecker.sys, "exit") as mock_exit:
                codechecker.init()
                assert mock_exit.call_args[0][0] == 42
