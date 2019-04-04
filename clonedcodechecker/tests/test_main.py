import unittest
import clonedcodechecker.clonedcodechecker as CCC


class MainUnitTest(unittest.TestCase):
    ccc = CCC.ClonedCodeChecker()

    def setUp(self):
        pass

    def test_launch(self):
        assert self.ccc.main()
