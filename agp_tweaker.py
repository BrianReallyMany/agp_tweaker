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
        self.ready_to_write[:] = []
        self.ready_to_write.append(self.first_line)
        self.first_line = self.second_line
        self.second_line = self.third_line
        self.third_line = newline

    def tweak_away(self):
        if len(self.second_line) == 0:
            return 
        elif self.second_line[4] == "W":
            sctg = self.second_line[5]
            tweak = self.tweaks_list.get_tweak_parameters(sctg)
            if len(tweak) != 0:
                if tweak[1] == "beginning":
                    self.tweak_begin(int(tweak[2]))
                else:
                    self.tweak_end(int(tweak[2]))
        else:
           return 

    def tweak_end(self, n):
        # Adjust column 3 of sctg
        old_sctg_end = int(self.second_line[2])
        new_sctg_end = str(old_sctg_end - n)
        self.second_line[2] = new_sctg_end
        # Adjust column 8 of sctg
        old_end = int(self.second_line[7])
        new_end = str(old_end - n)
        self.second_line[7] = new_end
        
        if self.third_line[4] != 'N':
            # make a new fragment
            self.ready_to_write.append(self.first_line)
            self.first_line = self.second_line
            self.second_line = self.make_new_fragment_after(self.first_line, n)
        else:
            # Adjust column 2 of fragment
            old_frag_begin = int(self.third_line[1])
            new_frag_begin = str(old_frag_begin - n)
            self.third_line[1] = new_frag_begin
            # Adjust column 6 of fragment
            old_length = int(self.third_line[5])
            new_length = str(old_length + n)
            self.third_line[5] = new_length

    def tweak_begin(self, n):
        # Adjust column 2 of sctg
        old_sctg_begin = int(self.second_line[1])
        new_sctg_begin = str(old_sctg_begin + n)
        self.second_line[1] = new_sctg_begin
        # Adjust column 8 of sctg
        old_end = int(self.second_line[7])
        new_end = str(old_end - n)
        self.second_line[7] = new_end

        if self.first_line[4] != 'N':
            # make new fragment
            self.ready_to_write.append(self.first_line)
            self.first_line = self.make_new_fragment_before(self.second_line, n)
        else:
            # Adjust column 3 of frag
            old_frag_end = int(self.first_line[2])
            new_frag_end = str(old_frag_end + n)
            self.first_line[2] = new_frag_end
            # Adjust column 6 of frag
            old_length = int(self.first_line[5])
            new_length = str(old_length + n)
            self.first_line[5] = new_length

    def make_new_fragment_after(self, line, n):
        previous_sctg_end = int(line[2])
        start = str(previous_sctg_end + 1)
        end = str(previous_sctg_end + n)
        frag_id = line[3] + ".5"
        frag = [line[0], start, end, frag_id, 'N', str(n), "fragment", "yes"]
        return frag

    def make_new_fragment_before(self, line, n):
        next_sctg_begin = int(line[1])
        start = str(next_sctg_begin - n)
        end = str(next_sctg_begin - 1)
        frag_id = str(int(line[3]) - 0.5)
        frag = [line[0], start, end, frag_id, 'N', str(n), "fragment", "yes"]
        return frag
        
        
        
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
            for line in buff.ready_to_write:
                if len(buff.ready_to_write[0]) > 0:
                    # (Avoids writing blank lines at beginning)
                    writer.writerow(line)    
        
        # Reached end of .agp, but still have rows in buffer.
        buff.update([])
        buff.tweak_away()
        for line in buff.ready_to_write:
            writer.writerow(line)
        buff.update([])
        buff.tweak_away()
        for line in buff.ready_to_write:
            writer.writerow(line)
        writer.writerow(buff.first_line)

## TODO need functionality to write a new fragment when trimming beginning of a sctg that is immediately preceded by another sctg (no fragment before) or trimming the end of one followed by another sctg (no fragment after)
## TODO more explicitly:
## TODO make ready_to_write a list of lines; pass tests
## TODO add check in tweak_begin, if first_line.is_sctg() then add first_line to ready_to_write, then first_line = create_frag(second_line, n), then tweak second_line
## TODO similarly, add check in tweak_end, if third_line.is_sctg() then add first_line to ready_to_write, tweak second_line, first_line = second_line, second_line = create_frag(first_line, n).
