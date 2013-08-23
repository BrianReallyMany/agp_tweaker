#!/usr/bin/env python

import csv

class AgpTweaker:


    def __init__(self):
        self.three_line_buffer = []
        self.tweaks_list = TweaksList()


    def sctg_needs_tweaking(self, sctg):
        for line in self.sctgs_to_tweak:
            if line[0] == sctg:
                return True
        return False


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


    def __init__(self, sctgs):
        self.sctgs_to_tweak = sctgs
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
            ## TODO refactor after create TweaksList class...
            print("foo")
        

    def sctg_needs_tweaking(self, sctg):
        for line in self.sctgs_to_tweak:
            if line[0] == sctg:
                return True
        return False

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
