import _common as common
class cppFile:

    __slots__ = ["filename", "lineset", "allLines", "blocks", "linestring"]

    # this is the constructor. when a cppFile gets loaded from filecache,
    # it gets created with a filename, lineset, allLines, blocks, and linestring
    # already populated (this happens in codeCache's addFile() method).
    # Otherwise, the file is loaded from source to populate these fields.
    def __init__(self, filename='', lineset=set(),
                 allLines=[], blocks=set(), linestring='', loaded=False):

        self.filename = filename
        self.lineset = lineset
        # lines do allow duplicates
        self.allLines = allLines
        # blocks are generic, larger units of code
        self.blocks = blocks
        self.linestring = linestring

        # setting loaded to True prevents this stuff from running. codeCache
        # passes True when it creates a cppFile that was already in it's filecache
        if not loaded:
            # opening a file this way will close it automatically when the 'with'
            # block finishes.
            with open(filename,'r') as file:
                lines = file.readlines()
            # strip whitespace out of each line ->
            # filter out blank lines and comment lines (defined in common.fun) ->
            # make a list of the result
            self.allLines = list(filter(common.fun,map(lambda x: x.strip(), lines)))
            # every line as one long string. we may want this for processing
            # large code blocks
            self.linestring = ''.join(self.allLines)
            # keeps only unique lines
            self.lineset = set(self.allLines)


    def printSet(self):
        for line in self.lineset:
            print(line)
