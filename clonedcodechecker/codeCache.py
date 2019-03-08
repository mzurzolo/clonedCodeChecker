import yaml
import cppFile as cpf
import os
import _common as common
import matcher as matchER
import hashlib
import matcher as matchER
try:
    from yaml import CSafeLoader as Loader
    from yaml import CSafeDumper as Dumper
except Exception:
    from yaml import SafeLoader as Loader
    from yaml import SafeDumper as Dumper


class codeCache():


    __slots__ = ["files", "searchSet", "filecache", "cachedfiles", "filelist", "matcher"]
    

    def __init__(self, files=None, searchSet=None,
                 filecache="./.filecache/", cachedfiles=None, filelist=None):

        self.files = set()
        self.searchSet = set()
        # the directory of processed files
        self.filecache = filecache
        self.cachedfiles = cachedfiles
        self.filelist = []
        
        self.matcher = matchER.matcher()

    # must be set after filecache is changed to the proper directory
    # in clonedCodeChecker.py
    def sync_cachedfiles(self):
        self.cachedfiles = set(os.listdir(self.filecache))

    def purge(self):
        for fname in os.listdir(self.filecache):
            os.remove(self.filecache + fname)
        self.cachedfiles = set(os.listdir(self.filecache))

    # add cppFile object to the codeCache. Use internally (from addFile())
    def add(self, cppfile):
        self.files.add(cppfile)

    # use this externally (from clonedCodeChecker's main())
    def addFile(self, filename):
        with open(filename, "rb") as tohash:
            hashed = hashlib.md5(tohash.read()).hexdigest()

        fname = common.cacheFileName(filename)
        self.filelist.append(fname)
        # if the file has been processed
        if fname in self.cachedfiles:
            # basic exception handling. try/except
            try:
                with open(self.filecache + fname, "r") as file:
                    # load up the file
                    data = yaml.load(file, Loader=Loader)
                    # grab all the fields
                    filename = data['filename']
                    hashed = data['hashed']
                    lineset = data['lineset']
                    allLines = []
                    blocks = data['blocks']
                    linestring = data['linestring']
                # successfully loaded
                print("load : ", filename)
                # create a new cppFile from loaded file, add it to codeCache
                self.add(cpf.cppFile(filename, lineset, allLines,
                                     blocks, linestring, hashed, True))
            # if there was a problem reading it, remove it from the filecache
            # directory and try to re-process from source.
            except Exception as e:
                print(e)
                os.remove(self.filecache + fname)
        # if the file isn't in the filecache, load/process it from source,
        # create a cppFile object, add it to codeCache
        else:
            self.add(cpf.cppFile(common.abspath(filename)))

    def saveCache(self):
        outdir = self.filecache
        # while the codeCache has cppFile objects:
        while len(self.files) > 0:
            # pop it off the set (and call it file)
            file = self.files.pop()
            # get a filecache name for it
            fname = common.cacheFileName(file.filename)
            # if the file is already in the filecache, skip the rest of this
            # loop and go back up to the while statement.
            if fname in self.cachedfiles:
                for line in file.lineset:
                    self.searchSet.add(line)
                continue

            for line in file.lineset:
                self.searchSet.add(line)

            # a dictionary makes it easy to dump cppFile's fields (and retrieve
            # them by name later)
            newdict = {}
            newdict["filename"] = file.filename
            newdict["hashed"] = file.hashed
            newdict["lineset"] = file.lineset
            newdict["linestring"] = file.linestring
            newdict["blocks"] = file.blocks

            # "{}{}".format(var1,var2) puts var1 and var2 into an empty string
            # another example:
            # "Var 1: {} here is var 2: {}... {}".format(1,2,"see?")
            # would produce the string: "Var 1: 1 here is var 2: 2... see?"
            with open("{}{}".format(outdir, fname), "w") as output:
                # save the dictionary to the filecache
                yaml.dump(newdict,
                          output,
                          Dumper=Dumper,
                          default_flow_style=False)

            print("saved : ", fname)
            # keep track of what gets added to the filecache directory so we
            # don't have to re-query the filesystem with os.listdir() as much
            self.cachedfiles.add(fname)

    def testmatch(self):
        for file in self.files:
            self.matcher.printMatches(file.linestring)


    def scanSearchSet(self):
        print(len(self.searchSet))
        for line in self.searchSet:
            input(line)
            
    def output(self):
        save_path = os.getcwd()
        #Create a file that the output will be put into
        name_of_file = "output_file: "
        completeName = os.path.join(save_path, name_of_file + ".txt")
        output_file = open(completeName, "a+")
        input_to_file = "matcher()"
        output_file.write(input_to_file)
        output_file.close()