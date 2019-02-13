#!/usr/bin/env python3

import yaml
import _common as common
class cppFile:

    __slots__ = ["filename", "lineset", "allLines", "blocks", "linestring"]


    def __init__(self, filename, load=False):
        if load:
            try:
                with open(filename, "r") as file:
                    data = yaml.load(file, Loader=yaml.CSafeLoader)
                    self.filename = data['filename']
                    self.lineset = data['lineset']
                    self.allLines = [] # data['allLines']
                    self.blocks = data['blocks']
                    self.linestring = data['linestring']

                print("load : ", filename)

            except Exception as e:
                os.remove(filename)
                load = False

        if not load:
            self.filename = filename
            # lines do allow duplicates
            self.allLines = []
            # blocks are generic, larger units of code
            self.blocks = set()

            with open(filename,'r') as file:
                lines = file.readlines()
                #for line in file:
                #    self.addLine( line.strip() )

                self.allLines = list(filter(common.fun,map(lambda x: x.strip(), lines)))
            #[line for line in self.allLines if
            #                 line[0] != "*" and line[0:1] != "/*"]

            self.linestring = ''.join(self.allLines)

            self.lineset = set(self.allLines)


    def addLine(self, line):
        self.allLines.append(line)
        #self.linestring += line


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
