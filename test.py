import unittest
import os

class TestExec(unittest.TestCase):

    def test_a3(self):
        self.assertTrue(os.path.isfile('build/exe.win32-3.5/a3.exe'))

if __name__ == '__main__':
    unittest.main()
