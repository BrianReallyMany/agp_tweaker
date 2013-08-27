#!/usr/bin/env python

import csv
import sys

class TweaksList:


    def __init__(self):
        self.tweaks = []

    def read_inputs(self, file_name):
        with open(file_name, 'rb') as inputs:
            reader = csv.reader(inputs, delimiter='\t', quotechar='|')
            for line in reader:
                self.tweaks.append(line)

    def get_tweak_parameters(self, sctg):
        for line in self.tweaks:
            if line[0] == sctg:
                return line
        return []


class AgpBuffer:


    def __init__(self, tweaks_list):
        self.tweaks_list = tweaks_list
        self.first_line = []
        self.second_line = []
        self.third_line = []
        self.ready_to_write = []

    def update(self, newline):
        self.ready_to_write = self.first_line
        self.first_line = self.second_line
        self.second_line = self.third_line
        self.third_line = newline

    def tweak_away(self):
        if len(self.second_line) == 0:
            return []
        elif self.second_line[4] == "W":
            sctg = self.second_line[5]
            tweak = self.tweaks_list.get_tweak_parameters(sctg)
            if len(tweak) != 0:
                if tweak[1] == "beginning":
                    self.tweak_begin(int(tweak[2]))
                else:
                    self.tweak_end(int(tweak[2]))
        else:
           return []

    def tweak_end(self, n):
        # Adjust column 3 of sctg
        old_sctg_end = int(self.second_line[2])
        new_sctg_end = str(old_sctg_end - n)
        self.second_line[2] = new_sctg_end
        # Adjust column 8 of sctg
        old_end = int(self.second_line[7])
        new_end = str(old_end - n)
        self.second_line[7] = new_end
        # Adjust column 2 of fragment
        old_frag_begin = int(self.third_line[1])
        new_frag_begin = str(old_frag_begin - n)
        self.third_line[1] = new_frag_begin
        # Adjust column 6 of fragment
        old_length = int(self.third_line[5])
        new_length = str(old_length + n)
        self.third_line[5] = new_length

    def tweak_begin(self, n):
        # Adjust column 3 of frag
        old_frag_end = int(self.first_line[2])
        new_frag_end = str(old_frag_end + n)
        self.first_line[2] = new_frag_end
        # Adjust column 6 of frag
        old_length = int(self.first_line[5])
        new_length = str(old_length + n)
        self.first_line[5] = new_length
        # Adjust column 2 of sctg
        old_sctg_begin = int(self.second_line[1])
        new_sctg_begin = str(old_sctg_begin + n)
        self.second_line[1] = new_sctg_begin
        # Adjust column 8 of sctg
        old_end = int(self.second_line[7])
        new_end = str(old_end - n)
        self.second_line[7] = new_end
        
        
############################
if __name__ == '__main__':
    
    # Check inputs ...
    if len(sys.argv) != 3:
        print("usage: python agp_tweaker.py <stuff-to-tweak file> <.agp file>")
        print("\nstuff-to-tweak file is tab-delimited in the format:")
        print("component_id     end/beginning   number of bases to delete")
        sys.exit()

    # Create TweaksList, AgpBuffer
    tl = TweaksList()
    tl.read_inputs(sys.argv[1])
    buff = AgpBuffer(tl)

    # Open .agp file and read first two lines into buffer
    with open(sys.argv[2]) as agp_file:
        reader = csv.reader(agp_file, delimiter='\t', quotechar='|')
        writer = csv.writer(sys.stdout, delimiter='\t', quoting=csv.QUOTE_NONE)
        for row in reader:
            buff.update(row)
            buff.tweak_away()
            writer.writerow(buff.ready_to_write)    
        
        # Reached end of .agp, but still have rows in buffer.
        buff.update([])
        buff.tweak_away()
        writer.writerow(buff.ready_to_write)
        buff.update([])
        buff.tweak_away()
        writer.writerow(buff.ready_to_write)
        writer.writerow(buff.first_line)

## TODO need functionality to write a new fragment when trimming beginning of a sctg that is immediately preceded by another sctg (no fragment before) or trimming the end of one followed by another sctg (no fragment after)
