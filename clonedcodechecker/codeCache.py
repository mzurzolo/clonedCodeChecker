#!/usr/bin/env python3

import yaml
import cppFile as cpf
import os
import _common as common

class codeCache():

    __slots__ = ["files", "stats", "filecache"]

    def __init__(self, files=None, stats=None, filecache="./.filecache/"):

        self.filecache = filecache

        if files:
            self.files = files
        else:
            self.files = set()
        if stats:
            self.stats = stats
        else:
            self.stats = {}


    def processFile(self, filename):
        if filename in self.files:
            return


    def printCache(self):
        for file in self.files:
            file.printSet()
#            file.buildBlocks()


    def add(self, cppfile):
        self.files.add(cppfile)




    def addFile(self, filename):
        fname = common.cacheFileName(filename)
        if fname in os.listdir(self.filecache):
            self.add(cpf.cppFile(os.path.abspath(self.filecache + fname),True))
        else:
            self.add(cpf.cppFile(os.path.abspath(filename)))


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
                yaml.dump(newdict,
                          output,
                          Dumper=yaml.CSafeDumper,
                          default_flow_style=False)

            print("saved : ", fname)
