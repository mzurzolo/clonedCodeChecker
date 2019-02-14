#!/usr/bin/env python3

import yaml
import _common as common
class cppFile:

    __slots__ = ["filename", "lineset", "allLines", "blocks", "linestring"]


    def __init__(self, filename='', lineset=set(),
                 allLines=[], blocks=set(), linestring='', loaded=False):

        self.filename = filename
        self.lineset = lineset
        # lines do allow duplicates
        self.allLines = allLines
        # blocks are generic, larger units of code
        self.blocks = blocks
        self.linestring = linestring

        if not loaded:
            with open(filename,'r') as file:
                lines = file.readlines()

            self.allLines = list(filter(common.fun,map(lambda x: x.strip(), lines)))
            self.linestring = ''.join(self.allLines)
            self.lineset = set(self.allLines)


    def addLine(self, line):
        self.allLines.append(line)


    def printSet(self):
        for line in self.lineset:
            print(line)
