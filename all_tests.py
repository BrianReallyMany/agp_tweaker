#!/urs/bin/env python

import unittest
from agp_tweaker import AgpTweaker

class TestStuff(unittest.TestCase):


    def test_read_inputs(self):
        tweaker = AgpTweaker()
        tweaker.read_inputs("test_files/test_input")
        self.assertEqual(2, len(tweaker.sctgs_to_tweak))



##########################
if __name__ == '__main__':
    unittest.main()
