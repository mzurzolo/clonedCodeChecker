"""code_cache holds the CodeCache and CppFile classes, and the YAML object."""

import os
from ruamel.yaml import YAML
import _common as common
import matcher

YA_ML = YAML(typ='safe')
YA_ML.default_style = False


class CodeCache():
    """The CodeCache holds CppFiles, the Matcher, and controls filecache."""

    __slots__ = ["files", "search_set", "filecache",
                 "cachedfiles", "filelist", "matcher"]

    def __init__(self, filecache="./.filecache/", cachedfiles=None):
        """Get new CodeCache object."""
        self.files = set()
        self.search_set = set()
        # the directory of processed files
        self.filecache = filecache
        self.cachedfiles = cachedfiles
        self.matcher = matcher.Matcher()

    # must be set after filecache is changed to the proper directory
    # in clonedCodeChecker.py
    def sync_cachedfiles(self):
        """Check what files are in the filecache."""
        self.cachedfiles = set(os.listdir(self.filecache))

    def purge(self):
        """Remove all files from the filecache."""
        for fname in os.listdir(self.filecache):
            os.remove(self.filecache + fname)
        self.cachedfiles = set(os.listdir(self.filecache))

    # use this externally (from clonedCodeChecker's main())
    def add_file(self, filename):
        """Add a new file to the CodeCache for analysis."""
        fname = common.cache_filename(filename)
        cachedfile = os.path.join(self.filecache, fname)
        new_file = CppFile(filename=filename, cachedfile=cachedfile)

        if fname in self.cachedfiles:
            try:
                if new_file.load_from_cache():
                    self.sync_cachedfiles()
            except Exception as e:
                print(e)
                os.remove(cachedfile)
                self.sync_cachedfiles()
        else:
            new_file.load_from_source()

        self.files.add(new_file)

    def save_cache(self):
        """Clear files out of memory, dumping new files into the filecache."""
        outdir = self.filecache
        # while the codeCache has cppFile objects:
        while self.files:
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

            with open(os.path.join(outdir, fname), "w") as outfile:
                YA_ML.dump(dict(file), outfile)
            print("saved : ", fname)
            # keep track of what gets added to the filecache directory so we
            # don't have to re-query the filesystem with os.listdir() as much
            self.cachedfiles.add(fname)
            # self.matcher.show_multiple()

    def testmatch(self):
        """Tell matcher to test the tokenizer."""
        for file in self.files:
            self.matcher.print_matches(file.linestring)

    def output(self, outputpath):
        """Tell matcher to print the report."""
        self.matcher.show_multiple(outputpath)


class CppFile:
    """CppFile represents a single loaded source file in the code_cache.

    filename: absolute path of source file
    cachedfile: absolute path of the cached version
    lineset: an unordered collection of unique lines in the file
    all_lines: all lines in the file
    blocks: collections of lines into logical pieces/blocks of code
    linestring: the whole file, in one big string. useful for the tokenizer
    t_modified: the last time the file was modified (epoch timestamp)
    as reported by the filesystem.
    """


    def __init__(self, filename, cachedfile=None):
        """Create new CppFile object."""
        self.filename = filename
        self.cachedfile = cachedfile
        self.lineset = None
        self.all_lines = None
        self.blocks = None
        self.linestring = None
        self.t_modified = os.stat(filename).st_mtime

    def keys(self):
        """Duck typing for dictionary."""
        return ['filename', 'cachedfile', 'lineset', 'all_lines',
                'blocks', 'linestring', 't_modified']

    def __getitem__(self, key):
        """Duck typing for dictionary."""
        return dict(zip(
                        ('filename', 'cachedfile', 'lineset', 'all_lines',
                         'blocks', 'linestring', 't_modified'),
                        (self.filename, self.cachedfile, self.lineset,
                         self.all_lines, self.blocks, self.linestring,
                         self.t_modified)))[key]

    def load_from_cache(self):
        """Try to load the file from the filecache.

        Returns False on successful load to tell the CodeCache it does not
        need to check the filecache for changes.
        """
        if self.cachedfile:
            # data = yaml.load(file)
            with open(self.cachedfile, 'r') as file:
                data = YA_ML.load(file)

            t_modified = data['t_modified']

            if self.t_modified == t_modified:
                # grab all the fields
                self.lineset = data['lineset']
                self.all_lines = data['all_lines']
                self.blocks = data['blocks']
                self.linestring = data['linestring']
                print("load : ", self.filename)
            else:
                os.remove(self.cachedfile)
                self.load_from_source()
                return True

        return False

    def load_from_source(self):
        """Load the file from the absolute path."""
        with open(self.filename, 'r') as file:
            lines = file.readlines()

        self.all_lines = lines
        # every line as one long string. we may want this for processing
        # large code blocks
        self.linestring = ''.join(self.all_lines)
        # keeps only unique lines
        self.lineset = set(self.all_lines)


# yaml.register_class(CppFile)
