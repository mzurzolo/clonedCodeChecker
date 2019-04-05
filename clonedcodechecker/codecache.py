"""code_cache holds the CodeCache and CppFile classes, and the YAML object."""

import os
from collections import deque, namedtuple
from ruamel.yaml import YAML
import clonedcodechecker._common as common
import clonedcodechecker.matcher as matcher

YA_ML_Dumper = YAML(typ='safe')
YA_ML_Loader = YAML(typ='safe')
YA_ML_Dumper.default_style = False
YA_ML_Loader.default_style = False
Token = namedtuple("Token", ['token', 'value', 'span'])


class CodeCache():
    """The CodeCache holds CppFiles, the Matcher, and controls filecache."""

    __slots__ = ["files", "search_set", "filecache",
                 "cachedfiles", "filelist", "matcher", "output_dir"]

    def __init__(self, filecache="./.filecache/", cachedfiles=None):
        """Get new CodeCache object."""
        self.files = deque()
        self.search_set = deque()
        # the directory of processed files
        self.filecache = filecache
        self.cachedfiles = cachedfiles
        self.matcher = matcher.Matcher()
        self.output_dir = None

    # must be set after filecache is changed to the proper directory
    # in clonedCodeChecker.py
    def sync_cachedfiles(self):
        """Check what files are in the filecache."""
        self.cachedfiles = set(os.listdir(self.filecache))

    def purge(self):
        """Remove all files from the filecache."""
        for fname in os.listdir(self.filecache):
            os.remove(os.path.join(self.filecache, fname))
        self.cachedfiles = set(os.listdir(self.filecache))

    def process_files(self):
        """Process files and save to filecache."""
        while self.search_set:
            self.save_file(self.add_file(self.search_set.pop()))

    def add_file(self, filename):
        """Add a new file to the CodeCache for analysis."""
        fname = common.cache_filename(filename)
        cachedfile = os.path.join(self.filecache, fname)

        if fname in self.cachedfiles:
            try:
                with open(cachedfile, 'r') as file:
                    new_file = YA_ML_Loader.load(file)
                if os.stat(filename).st_mtime == new_file['t_modified']:
                    print('reloaded: ----------------', filename)
                    return new_file
            except Exception as e:
                print(e)
                os.remove(cachedfile)
                self.sync_cachedfiles()
        new_file = CppFile(filename=filename)
        new_file.load_from_source()
        self.matcher.match_lines(new_file)
        print("loaded: --------------------", filename)
        return new_file

    def save_file(self, file):
        """Clear file out of memory, dumping new file into the filecache."""
        # get a filecache name for it
        fname = common.cache_filename(file.filename)
        filepath = os.path.join(self.filecache, fname)
        # match individual lines (for now)
        # if the file is already in the filecache, skip the rest of this
        # loop and go back up to the while statement.
        if fname in self.cachedfiles:
            print("returned")
            return

        with open(filepath, "w") as outfile:
            YA_ML_Dumper.dump(file, outfile)

        print("saved : ", fname)
        # keep track of what gets added to the filecache directory so we
        # don't have to re-query the filesystem with os.listdir() as much
        self.cachedfiles.add(fname)

    def testmatch(self):
        """Tell matcher to test the tokenizer."""
        for file in self.files:
            self.matcher.print_matches(file.linestring)

    def output(self):
        """Tell matcher to print the report."""
        self.matcher.print_output(self.output_dir)


class CppFile:
    """CppFile represents a single loaded source file in the code_cache.

    filename: absolute path of source file
    cachedfile: absolute path of the cached version
    lineset: an unordered collection of unique lines in the file
    all_lines: all lines in the file
    blocks: collections of lines into logical pieces/blocks of code
    t_modified: the last time the file was modified (epoch timestamp)
    as reported by the filesystem.
    """
    Token = namedtuple("Token", ['token', 'value', 'span'])

    def __init__(self, filename, cachedfile=None):
        """Create new CppFile object."""
        self.filename = filename
        self.cachedfile = cachedfile
        self.lineset = None
        self.tokenlist = None
        self.all_lines = None
        self.blocks = None
        self.t_modified = os.stat(filename).st_mtime

    def keys(self):
        """Duck typing for dictionary."""
        return ['filename', 'cachedfile', 'lineset', 'tokenlist', 'all_lines',
                'blocks', 't_modified']

    def __getitem__(self, key):
        """Duck typing for dictionary."""
        return dict(zip(
                        ('filename', 'cachedfile', 'lineset', 'tokenlist',
                         'all_lines', 'blocks', 't_modified'),
                        (self.filename, self.cachedfile, self.lineset,
                         self.tokenlist, self.all_lines, self.blocks,
                         self.t_modified)))[key]

    def load_from_source(self):
        """Load the file from the absolute path."""

        with open(self.filename, 'r') as file:
            lineread = file.read()

        self.all_lines = [splt_line.strip()
                          for splt_line in lineread.split('\n')]

        # keeps only unique lines
        self.lineset = set(self.all_lines)


YA_ML_Dumper.register_class(CppFile)
YA_ML_Loader.register_class(CppFile)
