#!/usr/bin/env python3

import yaml

class codeCache():

    __slots__ = ["files", "stats"]

    def __init__(self, files=None, stats=None, cacheFile="../filecache/filecache.yaml"):
        try:
            with open(cacheFile,"r") as file:
                data = yaml.safe_load(f)
            input(data)
        except:
            print("Error loading {} ... starting fresh".format(cacheFile))
            if files:
                self.files = files
            else:
                self.files = set()
            if stats:
                self.stats = stats
            else:
                self.stats = {}

    def processFile(self, filename):
        if filename in files:
            return

    def addFile(self, cppfile):
        self.files.add(cppfile)

    def printCache(self):
        for file in self.files:
            file.printSet()
#            file.buildBlocks()

    def saveCache(self, outfile="./filecache/filecache.yaml"):
        with open(outfile,"w") as output:
            for file in self.files:
                yaml.safe_dump(file.allLines)
