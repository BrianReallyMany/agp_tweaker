#!/usr/bin/env python

import csv

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
        if self.second_line[4] == "W":
            sctg = self.second_line[5]
            tweak = self.tweaks_list.get_tweak_parameters(sctg)
            if len(tweak) != 0:
                print("got to tweak")
            else:
                print("no tweaks here")
                return []

    def tweak_end(self, n):
        old_sctg_end = int(self.second_line[2])
        new_sctg_end = str(old_sctg_end - n)
        self.second_line[2] = new_sctg_end
        old_frag_begin = int(self.third_line[1])
        new_frag_begin = str(old_frag_begin - n)
        self.third_line[1] = new_frag_begin

    def tweak_begin(self, n):
        old_frag_end = int(self.first_line[2])
        new_frag_end = str(old_frag_end + n)
        self.first_line[2] = new_frag_end
        old_sctg_begin = int(self.second_line[1])
        new_sctg_begin = str(old_sctg_begin + n)
        self.second_line[1] = new_sctg_begin
        
        

## main should be something like:
## tweek = AgpTweaker()
## tweek.read_inputs(args[0])
## reader = AgpReader()
## (maybe the constructor should create reader and buffer?)
## buff = AgpBuffer()
## read first 2 lines into buffer (buff.update(firstline), etc.)
## run buff.check_middle_line, which updates lines 1-3 if necessary
## writer = AgpWriter(args[1]) -- or else stdout?
## while reader.hasnext() do
##   writer.write(buff.ready_to_write)
##   buff.update(reader.getnext())
## then when reader has no next,
## buffer should contain last 3 lines,
## so buff.process_last_two or s.th.?
##
## so ...
## TODO AgpBuffer methods for actually updating shit
##      (check if second_line is sctg, if so check if
##      on list, if so do stuff ...)
## TODO AgpReader, AgpWriter
## TODO AgpBuffer method for processing last of the data, maybe
##      can be real slick about this...
## TODO what if need to tweak same sctg at begin *and* end???
