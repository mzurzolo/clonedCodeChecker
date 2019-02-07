#!/usr/bin/env python3

class cppFile:

    __slots__ = ["filename", "lineset", "allLines"]


    def __init__(self, filename):
        self.filename = filename
        # sets do not allow duplicates (it's like a hashset)
        self.lineset = set()
        # lines do allow duplicates
        self.allLines = []

    def addLine(self, line):
        self.lineset.add(line)
        self.allLines.append(line)


    def printSet(self):
        for line in self.lineset:
            print(line)
