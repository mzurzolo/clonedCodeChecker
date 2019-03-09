
import hashlib


class cppFile:

    __slots__ = ["filename", "lineset", "allLines", "blocks", "linestring"]

    # this is the constructor. when a cppFile gets loaded from filecache,
    # it gets created with a filename, lineset, allLines, blocks, and
    # linestring already populated (this happens in codeCache's addFile()
    # method). Otherwise, the file is loaded from source to populate these
    # fields.
    def __init__(self, filename='', lineset=None,
                 allLines=None, blocks=None, linestring='', loaded=False):

        self.filename = filename
        # sets do not allow duplicates
        if not lineset:
            self.lineset = set()
        else:
            self.lineset = lineset
        # blocks are generic, larger units of code
        if not blocks:
            self.blocks = set()
        else:
            self.blocks = blocks
        # lists do allow duplicates
        if not allLines:
            self.allLines = []
        else:
            self.allLines = allLines

        self.linestring = linestring

        # setting loaded to True prevents this stuff from running. codeCache
        # passes True when it creates a cppFile that was already in it's
        # filecache
        if not loaded:
            with open(filename, 'r') as file:
                lines = file.readlines()

            self.allLines = lines
            # every line as one long string. we may want this for processing
            # large code blocks
            self.linestring = ''.join(self.allLines)
            # keeps only unique lines
            self.lineset = set(self.allLines)

    def printSet(self):
        for line in self.lineset:
            print(line)
