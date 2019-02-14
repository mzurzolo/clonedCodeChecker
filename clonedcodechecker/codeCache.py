#!/usr/bin/env python3

import yaml
import cppFile as cpf
import os
import _common as common

class codeCache():

    __slots__ = ["files", "stats", "filecache", "filecachelistdir"]

    def __init__(self, files=None, stats=None, filecache="./.filecache/"):

        self.filecache = filecache
        self.filecachelistdir = set(os.listdir(self.filecache))

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


    def add(self, cppfile):
        self.files.add(cppfile)


    def addFile(self, filename):
        fname = common.cacheFileName(filename)
        if fname in self.filecachelistdir:
            try:
                with open(self.filecache + fname, "r") as file:
                    data = yaml.load(file, Loader=yaml.CSafeLoader)
                    filename = data['filename']
                    lineset = data['lineset']
                    allLines = [] # data['allLines']
                    blocks = data['blocks']
                    linestring = data['linestring']

                print("load : ", filename)
                self.add(cpf.cppFile(filename, lineset, allLines,
                                     blocks, linestring, True))

            except Exception as e:
                print(e)
                os.remove(filename)
        else:
            self.add(cpf.cppFile(os.path.abspath(filename)))


    def saveCache(self, outdir="./.filecache/"):
        while len(self.files) > 0:
            file = self.files.pop()
            fname = common.cacheFileName(file.filename)

            if fname in self.filecachelistdir:
                # print("_______________________________________________________")
                continue

            newdict = {}
            newdict["filename"] = file.filename
            newdict["lineset"] = file.lineset
            newdict["linestring"] = file.linestring
            newdict["blocks"] = file.blocks

            with open("{}{}".format(outdir, fname), "w") as output:
                yaml.dump(newdict,
                          output,
                          Dumper=yaml.CSafeDumper,
                          default_flow_style=False)

            print("saved : ", fname)
            self.filecachelistdir.add(fname)
