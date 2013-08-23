#!/urs/bin/env python

import unittest
from agp_tweaker import AgpBuffer, TweaksList


class TestTweaksList(unittest.TestCase):


    def test_initialize(self):
        tl = TweaksList()
        self.assertEqual(0, len(tl.tweaks))

    def test_read_inputs(self):
        tl = TweaksList()
        tl.read_inputs("test_files/test_input")
        self.assertEqual(2, len(tl.tweaks))

    def test_get_tweak_parameters(self):
        tl = TweaksList()
        line1 = ["sctg_0001_0001", "end", "3"]
        line2 = ["sctg_0001_0003", "beginning", "5"]
        tl.tweaks = [line1, line2]
        result1 = tl.get_tweak_parameters("sctg_0001_0003")
        self.assertEqual(3, len(result1))
        result2 = tl.get_tweak_parameters("sctg_0001_0002")
        self.assertEqual(0, len(result2))

        

class TestAgpBuffer(unittest.TestCase):


    def test_initialize(self):
        buff = AgpBuffer([])
        self.assertEqual(0, len(buff.first_line))

    def test_update(self):  
        buff = AgpBuffer([])
        new_line = ["foo", "bar"]
        buff.update(new_line)
        self.assertEqual("foo", buff.third_line[0])

    def test_tweak_away(self):
        sctg1 = ["sctg_0001_0001", "end", "3"]
        sctg2 = ["sctg_0001_0003", "beginning", "5"]
        sctgs = [sctg1, sctg2]
        buff = AgpBuffer(sctgs)
        sctg =  """scaffold00001    1   4968    1   W   sctg_0001_0001  1   4968    +""".split()
        frag = """scaffold00001 4969    6317    2   N   1349    fragment    yes""".split()
        buff.update(sctg)
        buff.update(frag)
        buff.tweak_away()
        #self.assertEqual(4965, buff.second_line[2])
        # goes like this: read frag/sctg/frag into buffer,
        # call buff.tweak_away()
        # buff will call "needs_tweaking" on second_line
        # need to pass sctgs_to_tweak to buffer on create? i guess
        # anyway buffer will check sctgs to tweak and should
        # get a yes, adjust indices, pau.
        # once this works the program is basically wrote.
        


##########################
if __name__ == '__main__':
    unittest.main()
