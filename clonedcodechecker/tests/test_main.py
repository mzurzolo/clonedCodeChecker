import unittest
import clonedcodechecker as CCC
print(dir())
print(dir(CCC))
print(dir(CCC.clonedcodechecker))
print(dir(CCC.clonedcodechecker.ClonedCodeChecker()))


class MainUnitTest(unittest.TestCase):
    ccc = CCC.ClonedCodeChecker()

    def setUp(self):
        pass

    def test_launch(self):
        assert self.ccc.main()
