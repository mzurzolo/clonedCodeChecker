import os
import yaml
try:
    from yaml import CSafeLoader as Loader
    from yaml import CSafeDumper as Dumper
except Exception:
    from yaml import SafeLoader as Loader
    from yaml import SafeDumper as Dumper
import CppFile as cpf
import _common as common
import matcher

class CodeCache():

    __slots__ = ["files", "searchSet", "filecache",
                 "cachedfiles", "filelist", "matcher"]

    def __init__(self, files=None, searchSet=None,
                 filecache="./.filecache/", cachedfiles=None,
                 filelist=None, lineMatches=None):

        self.files = set()
        self.searchSet = set()
        # the directory of processed files
        self.filecache = filecache
        self.cachedfiles = cachedfiles
        self.matcher = matcher.Matcher()

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

        fname = common.cache_filename(filename)
        # if the file has been processed
        new_t_modefied = os.stat(filename).st_mtime
        if fname in self.cachedfiles:
            # basic exception handling. try/except
            try:
                with open(self.filecache + fname, "r") as file:
                    data = yaml.load(file, Loader=Loader)
                # grab all the fields
                filename = data['filename']
                lineset = data['lineset']
                allLines = [] # data['allLines']
                blocks = data['blocks']
                linestring = ''# data['linestring']
                t_modefied = data['t_modefied']
                if new_t_modefied == t_modefied:
                    # successfully loaded
                    print("load : ", filename)
                    # create a new cppFile from loaded file and
                    # add it to codeCache
                    self.add(cpf.CppFile(filename=filename,
                                         lineset=lineset,
                                         allLines=allLines,
                                         blocks=blocks,
                                         linestring=linestring,
                                         t_modefied=t_modefied,
                                         loaded=True))

                else:
                    os.remove(self.filecache + fname)
                    self.sync_cachedfiles()
                    self.add(cpf.CppFile(
                        filename=common.abspath(filename),
                        t_modefied=new_t_modefied))

            # if there was a problem reading it, remove it from the filecache
            # directory and try to re-process from source.
            except Exception as e:
                print(e)
                os.remove(self.filecache + fname)
                self.add(cpf.CppFile(
                    filename=common.abspath(filename),
                    t_modefied=new_t_modefied))
        # if the file isn't in the filecache, load/process it from source,
        # create a cppFile object, add it to codeCache
        else:
            self.add(cpf.CppFile(filename=common.abspath(filename),
                                 t_modefied=new_t_modefied))

    def saveCache(self):
        outdir = self.filecache
        # while the codeCache has cppFile objects:
        while len(self.files) > 0:
            # pop it off the set (and call it file)
            file = self.files.pop()
            # get a filecache name for it
            fname = common.cache_filename(file.filename)

            # match individual lines (for now)
            self.matcher.match_lines(fname, file.lineset)
            # if the file is already in the filecache, skip the rest of this
            # loop and go back up to the while statement.
            if fname in self.cachedfiles:
                continue
            # a dictionary makes it easy to dump cppFile's fields (and retrieve
            # them by name later)
            newdict = {}
            newdict["filename"] = file.filename
            newdict["lineset"] = file.lineset
            # newdict["allLines"] = file.allLines
            newdict["blocks"] = file.blocks
            newdict["t_modefied"] = file.t_modefied
            # newdict["linestring"] = file.linestring
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
            # self.matcher.show_multiple()

    def testmatch(self):
        for file in self.files:
            self.matcher.print_matches(file.linestring)

    def scanSearchSet(self):
        print(len(self.searchSet))
        for line in self.searchSet:
            input(line)

    def output(self, outputpath):
        self.matcher.show_multiple(outputpath)