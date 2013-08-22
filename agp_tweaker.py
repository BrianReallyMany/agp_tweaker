#!/usr/bin/env python

import csv

class AgpTweaker:
    sctgs_to_tweak = []


    def read_inputs(self, file_name):
        with open(file_name, 'rb') as inputs:
            reader = csv.reader(inputs, delimiter='\t', quotechar='|')
            for line in reader:
                self.sctgs_to_tweak.append(line)
                
