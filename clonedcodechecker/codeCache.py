#!/usr/bin/env python3

import yaml
import cppFile as cpf
import os
import _common as common

class codeCache():

    __slots__ = ["files", "stats"]

    def __init__(self, files=None, stats=None, filecache="./.filecache/"):
        #with open(cacheFile,"r") as file:
            #for line in file:
                #print(line)
        if files:
            self.files = files
        else:
            self.files = set()
        if stats:
            self.stats = stats
        else:
            self.stats = {}

        try:
            for file in os.listdir(filecache):
                self.loadFile(filecache + file)


        except:
            print("Error loading {} ... starting fresh".format(filecache))


    def processFile(self, filename):
        if filename in self.files:
            return


    def addFile(self, cppfile):
        self.files.add(cppfile)


    def printCache(self):
        for file in self.files:
            file.printSet()
#            file.buildBlocks()


    def loadFile(self, filename):
        #input(os.path.abspath(filename))
        self.addFile(cpf.cppFile(os.path.abspath(filename),True))


    def saveCache(self, outdir="./.filecache/"):
        while len(self.files) > 0:
            file = self.files.pop()
            fname = common.cacheFileName(file.filename)

            if fname in os.listdir(outdir):
                print("_______________________________________________________")
                continue

            newdict = {}
            newdict["filename"] = file.filename
            newdict["lineset"] = file.lineset
            newdict["allLines"] = file.allLines
            newdict["blocks"] = file.blocks

            with open("{}{}".format(outdir, fname), "w") as output:
                yaml.dump(newdict, output, Dumper=yaml.CSafeDumper)

            print("saved : ", fname)
