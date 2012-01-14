
import os
import unittest

from simplecache import *

#TODO: import from simplecache
SIMPLECACHE_DIR = os.path.join(os.getcwd(), '.cache')

def test_func(*args):
    out = 0
    for arg in args:
        out += arg
    return out

class TestBaseClass(unittest.TestCase):

    def setUp(self):
        pass

    def test_initial(self):
        cache(test_func, [1,2])


    def tearDown(self):
        pass

if __name__ == "__main__":
    unittest.main()
    print ("Bond")
