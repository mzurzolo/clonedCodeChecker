import unittest
import pytest
import mock
import os


class MockedCodeCache(unittest.TestCase):
    # thank you https://medium.com/opsops/how-to-test-if-name-main-1928367290cb
    def test_run():
        from clonedcodechecker import codechecker

        with mock.patch.object(codechecker, "main", return_value=42):
            with mock.patch.object(codechecker, "__name__", "__main__"):
                with mock.patch.object(codechecker.sys, "exit") as mock_exit:
                    codechecker.run()
                    assert mock_exit.call_args[0][0] == 42


class MockedClonedCodeChecker(unittest.TestCase):
    from clonedcodechecker.codechecker import ClonedCodeChecker

    codechecker_autospec = unittest.mock.create_autospec(ClonedCodeChecker)


class MockedMatcher(unittest.TestCase):
    from clonedcodechecker.matcher import Matcher

    matcher_autospec = unittest.mock.create_autospec(Matcher)


class MockedMergeUpdater(unittest.TestCase):
    from clonedcodechecker.matcher import MergeUpdater

    mergeupdater_autospec = unittest.mock.create_autospec(MergeUpdater)


class MockedClonedCodeChecker(unittest.TestCase):
    from clonedcodechecker.codecache import CodeCache

    codecache_autospec = unittest.mock.create_autospec(CodeCache)
