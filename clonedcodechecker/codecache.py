"""code_cache holds the CodeCache and CppFile classes, and the YAML object."""

import os
from collections import deque, defaultdict
from ruamel.yaml import YAML
from clonedcodechecker.matcher import Matcher

YA_ML = YAML(typ="safe")
YA_ML.default_style = False


def cache_filename(path):
    """Turn absolute path into filename used in filecache."""
    return path.replace("/", ".")[1:] + ".yaml"


class CodeCache:
    """The CodeCache holds CppFiles, the Matcher, and controls filecache.

    Slots:
    search_set: Absolute paths of all files to search. Comes from codechecker
    filecache: Directory of the filecache. It's always in ~/.filecache
    matcher: The CodeCache owns an instance of the Matcher class
    output_dir: Set externally (in codechecker) on program launch
    """

    __slots__ = [
        "search_set",
        "filecache",
        "filelist",
        "matcher",
        "output_dir",
    ]

    def __init__(self, filecache="./.filecache/"):
        """Get new CodeCache object."""
        self.search_set = deque()
        self.filecache = filecache
        self.matcher = Matcher()
        self.output_dir = None

    def purge(self):
        """Remove all files from the filecache."""
        for fname in os.listdir(self.filecache):
            os.remove(os.path.join(self.filecache, fname))

    def process_files(self):
        """Process files and save to filecache."""
        while self.search_set:
            current_file = self.add_file(self.search_set.pop())
            self.save_file(current_file)

    def add_file(self, filename):
        """Add a new file to the CodeCache for analysis."""
        # Get the filename that will be used for the filecache
        fname = cache_filename(filename)
        # Full path for the file in the filecache
        cachedfile = os.path.join(self.filecache, fname)
        # Last time the file was modefied
        t_modified = os.stat(filename).st_mtime
        print(filename)
        try:
            # Try to get it from the filecache
            with open(cachedfile, "r") as file:
                new_file = YA_ML.load(file)
            if new_file.t_modified != t_modified:
                os.remove(cachedfile)
                raise OSError
        except (OSError, FileNotFoundError):
            # Create a new CppFile if the above fails. It will fail on
            # Differing timestamps, and on file not being in the filecache.
            new_file = CppFile(
                filename=filename, cachedfile=cachedfile, t_modified=t_modified
            )
            # Get members. This only runs if the file needs to be processed
            # or re-processed.
            member_tokens, linesize = self.matcher.tokenize(new_file.linestring)
            new_file.linesize = linesize
            new_file.member_tokens = list(member_tokens)
        # matcher's linesize is updated here to account for files that do not
        # need to go through mathcer.tokenize  (where the count is generated)
        self.matcher.total_linecount += new_file.linesize
        # Further processing of members could happen here, before they go to
        # match_tokens
        self.matcher.match_tokens(new_file.filename, new_file.member_tokens)
        # return to process_files, which dumps it directly to save_file
        return new_file

    def save_file(self, file):
        """Clear file out of memory, dumping new file into the filecache."""
        # get a filecache name for it
        fname = cache_filename(file.filename)
        filepath = os.path.join(self.filecache, fname)
        file.linestring = ""
        # if the file is already in the filecache, skip the rest of this
        # loop and go back up to the while statement.
        try:
            with open(filepath, "x") as outfile:
                YA_ML.dump(file, outfile)
        except FileExistsError:
            pass

    def output(self, starttime=None, filecount=None):
        """Tell matcher to print the report."""
        self.matcher.print_output(
            self.output_dir, starttime=starttime, filecount=filecount
        )


class CppFile(defaultdict):
    """CppFile represents a single loaded source file in the code_cache.

    filename: absolute path of source file
    cachedfile: absolute path of the cached version
    lineset: an unordered collection of unique lines in the file
    all_lines: all lines in the file
    blocks: collections of lines into logical pieces/blocks of code
    t_modified: the last time the file was modified (epoch timestamp)
    as reported by the filesystem.
    """

    def __init__(
        self,
        filename=None,
        cachedfile=None,
        t_modified=None,
        linesize=None,
        member_tokens=None,
    ):
        """Create new CppFile object."""
        self.filename = filename
        self.cachedfile = cachedfile
        self.t_modified = t_modified
        self.linesize = linesize
        self.member_tokens = member_tokens
        self.__loadall__()

    def __loadall__(self):
        """Load the file from the filecache or from the absolute path."""
        with open(self.filename, "r", errors="ignore") as file:
            self.linestring = file.read()


# class must be registered to be loadable/dumpable by the C implementation
YA_ML.register_class(CppFile)
