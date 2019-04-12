"""code_cache holds the CodeCache and CppFile classes, and the YAML object."""

import os
from collections import deque, UserDict
from ruamel.yaml import YAML
from clonedcodechecker.matcher import Matcher

YA_ML = YAML(typ='safe')
YA_ML.default_style = False


def cache_filename(path):
    """Turn absolute path into filename used in filecache."""
    return path.replace("/", ".")[1:] + ".yaml"


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
        self.matcher = Matcher()
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
            current_file = self.add_file(self.search_set.pop())
            self.matcher.match_lines(current_file)
            all_tokens = self.matcher.get_tokens(current_file.linestring)
            #for t in all_tokens:
            #    input(t)
            self.save_file(current_file)

    def add_file(self, filename):
        """Add a new file to the CodeCache for analysis."""
        # Get the filename that will be used for the filecache
        fname = cache_filename(filename)
        # Full path for the file in the filecache
        cachedfile = os.path.join(self.filecache, fname)
        # Last time the file was modefied
        t_modified = os.stat(filename).st_mtime

        try:
            with open(cachedfile, 'r') as file:
                new_file = YA_ML.load(file)
            if new_file.t_modified != t_modified:
                os.remove(cachedfile)
                raise OSError
        except (OSError, FileNotFoundError) as e:
            new_file = CppFile(filename=filename,
                               cachedfile=cachedfile,
                               t_modified=t_modified)

        self.matcher.match_lines(new_file)
        print("loaded: --------------------", filename)
        return new_file

    def save_file(self, file):
        """Clear file out of memory, dumping new file into the filecache."""
        # get a filecache name for it
        fname = cache_filename(file.filename)
        filepath = os.path.join(self.filecache, fname)
        # match individual lines (for now)
        # if the file is already in the filecache, skip the rest of this
        # loop and go back up to the while statement.
        try:
            with open(filepath, "x") as outfile:
                YA_ML.dump(file, outfile)
        except FileExistsError:
            pass

        print("saved : ", fname)

    def testmatch(self):
        """Tell matcher to test the tokenizer."""
        for file in self.files:
            self.matcher.print_matches(file.linestring)

    def output(self):
        """Tell matcher to print the report."""
        self.matcher.print_output(self.output_dir)


class CppFile(UserDict):
    """CppFile represents a single loaded source file in the code_cache.

    filename: absolute path of source file
    cachedfile: absolute path of the cached version
    lineset: an unordered collection of unique lines in the file
    all_lines: all lines in the file
    blocks: collections of lines into logical pieces/blocks of code
    t_modified: the last time the file was modified (epoch timestamp)
    as reported by the filesystem.
    """

    def __init__(self, filename=None, cachedfile=None, t_modified=None):
        """Create new CppFile object."""
        self.filename = filename
        self.cachedfile = cachedfile
        self.t_modified = t_modified
        self.__loadall__()

    def __loadall__(self):
        """Load the file from the filecache or from the absolute path."""
        with open(self.filename, 'r') as file:
            self.linestring = file.read()

        self.all_lines = [splt_line.strip()
                          for splt_line in self.linestring.split('\n')]

        # keeps only unique lines
        self.lineset = set(self.all_lines)


YA_ML.register_class(CppFile)
