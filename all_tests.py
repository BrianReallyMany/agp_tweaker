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
        tl = TweaksList()
        sctg1 = ["sctg_0001_0001", "end", "3"]
        sctg2 = ["sctg_0001_0003", "beginning", "5"]
        tl.tweaks = [sctg1, sctg2]
        buff = AgpBuffer(tl)
        sctg =  """scaffold00001    1   4968    1   W   sctg_0001_0001  1   4968    +""".split()
        frag = """scaffold00001 4969    6317    2   N   1349    fragment    yes""".split()
        buff.update(sctg)
        buff.update(frag)
        buff.tweak_away()
        self.assertEqual("4965", buff.second_line[2])

    def test_tweak_end(self):
        buff = AgpBuffer([])
        sctg =  """scaffold00001    1   4968    1   W   sctg_0001_0001  1   4968    +""".split()
        frag = """scaffold00001 4969    6317    2   N   1349    fragment    yes""".split()
        buff.update(sctg)
        buff.update(frag)
        buff.tweak_end(5)
        self.assertEqual("4963", buff.second_line[2])
        self.assertEqual("4964", buff.third_line[1])

    def test_tweak_begin(self):
        buff = AgpBuffer([])
        frag1 = """scaffold00001    4969    6317    2   N   1349    fragment    yes""".split()
        sctg = """scaffold00001 6318    13067   3   W   sctg_0001_0002  1   6750    +""".split()
        frag2 = """scaffold00001    13068   14934   4   N   1867    fragment    yes""".split()
        buff.update(frag1)
        buff.update(sctg)
        buff.update(frag2)
        buff.tweak_begin(7)
        self.assertEqual("6324", buff.first_line[2])

        


##########################
if __name__ == '__main__':
    unittest.main()
