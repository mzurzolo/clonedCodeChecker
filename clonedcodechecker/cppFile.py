#!/usr/bin/env python3

class cppFile:

    __slots__ = ["filename", "lineset", "allLines", "blocks"]


    def __init__(self, filename):
        self.filename = filename
        # sets do not allow duplicates (it's like a hashset)
        self.lineset = set()
        # lines do allow duplicates
        self.allLines = []
        # blocks are generic, larger units of code
        self.blocks = set()

        with open(filename,'r') as file:
            for line in file:
                self.addLine( line.strip() )


    def addLine(self, line):
        self.lineset.add(line)
        self.allLines.append(line)


#    def buildBlocks(self):
#        print(self.filename)
#        for line in self.allLines:
#            if len(line) > 0:
#                if line[0] == "*":
#                    continue
#                if line.find("{") > -1:
#                    input(line)


    def printSet(self):
        for line in self.lineset:
            print(line)
