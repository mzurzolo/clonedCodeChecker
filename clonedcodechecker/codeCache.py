#!/usr/bin/env python3

import yaml
import cppFile as cpf
import os
import _common as common
try:
    from yaml import CSafeLoader as Loader
    from yaml import CSafeDumper as Dumper
except:
    from yaml import SafeLoader as Loader
    from yaml import SafeDumper as Dumper

class codeCache():

    __slots__ = ["files", "searchSet", "filecache", "filecachelistdir"]

    def __init__(self, files=set(), searchSet=set(), filecache="./.filecache/"):

        self.files = files
        self.searchSet = searchSet
        # the directory of processed files
        self.filecache = filecache
        # the files in filecache
        self.filecachelistdir = set(os.listdir(self.filecache))


    # for debugging. prints lots of lines
    def printCache(self):
        for file in self.files:
            file.printSet()

    def purge(self):
        os.rmdir(self.filecache)

    # add cppFile object to the codeCache. Use internally (from addFile())
    def add(self, cppfile):
        self.files.add(cppfile)


    # use this externally (from clonedCodeChecker's main())
    def addFile(self, filename):
        fname = common.cacheFileName(filename)
        # if the file has been processed
        if fname in self.filecachelistdir:
            # basic exception handling. try/except
            try:
                with open(self.filecache + fname, "r") as file:
                    # load up the file
                    data = yaml.load(file, Loader=Loader)
                    # grab all the fields
                    filename = data['filename']
                    lineset = data['lineset']
                    allLines = [] # data['allLines']
                    blocks = data['blocks']
                    linestring = data['linestring']
                # successfully loaded
                print("load : ", filename)
                # create a new cppFile from loaded file, add it to codeCache
                self.add(cpf.cppFile(filename, lineset, allLines,
                                     blocks, linestring, True))
            # if there was a problem reading it, remove it from the filecache
            # directory and try to re-process from source.
            except Exception as e:
                print(e)
                os.remove(self.filecache + fname)
        # if the file isn't in the filecache, load/process it from source, create a
        # cppFile object, add it to codeCache
        else:
            self.add(cpf.cppFile(common.abspath(filename)))


    def saveCache(self, outdir="./.filecache/"):
        # while the codeCache has cppFile objects:
        while len(self.files) > 0:
            # pop it off the set (and call it file)
            file = self.files.pop()
            # get a filecache name for it
            fname = common.cacheFileName(file.filename)
            # if the file is already in the filecache, skip the rest of this loop
            # and go back up to the while statement.
            if fname in self.filecachelistdir:
                for line in file.lineset:
                    self.searchSet.add(line)
                continue

            for line in file.lineset:
                self.searchSet.add(line)

            # a dictionary makes it easy to dump cppFile's fields (and retrieve
            # them by name later)
            newdict = {}
            newdict["filename"] = file.filename
            newdict["lineset"] = file.lineset
            newdict["linestring"] = file.linestring
            newdict["blocks"] = file.blocks

            # "{}{}".format(var1,var2) inserts var1 and var2 into an empty string
            # another example: "Var 1: {} here is var 2: {}... {}".format(1,2,"see?")
            # would produce the string: "Var 1: 1 here is var 2: 2... see?"
            with open("{}{}".format(outdir, fname), "w") as output:
                # save the dictionary to the filecache
                yaml.dump(newdict,
                          output,
                          Dumper=Dumper,
                          default_flow_style=False)

            print("saved : ", fname)
            # keep track of what gets added to the filecache directory so we
            # don't have to re-query the filesystem with os.listdir() all the time
            self.filecachelistdir.add(fname)


    def scanSearchSet(self):
        print(len(self.searchSet))
        for line in self.searchSet:
            input(line)