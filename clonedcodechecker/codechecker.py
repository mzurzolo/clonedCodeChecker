"""The clonedcodechecker is a static analysis tool for C/C++ Source Code."""

import os
import sys
import argparse
from collections import deque
from datetime import datetime
from clonedcodechecker.codecache import CodeCache
from clonedcodechecker._version import __version__ as version


class ClonedCodeChecker:
    """The ClonedCodeChecker collects files for its CodeCache."""

    def __init__(
        self,
        output_location=".",
        filecache_location=".",
        starttime=datetime.now(),
    ):
        """Get new ClonedCodeChecker object."""
        self.code_cache = CodeCache()
        self.output_location = output_location
        self.filecache_location = filecache_location
        self.starttime = starttime
        try:
            os.mkdir(self.filecache_location)
        except FileExistsError:
            pass

    # "directory="." " means that directory is optional. If load_cpp_files is
    # not passed a directory, it uses ".", which is the current directory
    def load_cpp_files(self, directory="."):
        """Iterate through the list of files in directory, load them."""
        absolute_files = [
            os.path.realpath(file.path)
            for file in os.scandir(directory)
            if file.is_file() and not file.name.startswith(".")
        ]

        source_c_files = [
            file
            for file in absolute_files
            if file.endswith(
                (
                    ".cpp",
                    ".Cpp",
                    ".cPp",
                    ".cpP",
                    ".CPp",
                    ".cPP",
                    ".CpP",
                    ".CPP",
                    ".C",
                    ".c",
                )
            )
        ]

        filecount = len(source_c_files)
        self.code_cache.search_set.extend(source_c_files)
        self.code_cache.process_files()
        self.code_cache.output(starttime=self.starttime, filecount=filecount)

    def recursive_walk(self, directory="."):
        """Recursive directory walk."""
        cfiles = deque()
        for current, _folders, files in os.walk(directory):
            absolute_files = [
                os.path.join(os.path.realpath(current), file)
                for file in files
                if not file.startswith(".")
            ]

            source_c_files = [
                file
                for file in absolute_files
                if file.endswith(
                    (
                        ".cpp",
                        ".Cpp",
                        ".cPp",
                        ".cpP",
                        ".CPp",
                        ".cPP",
                        ".CpP",
                        ".CPP",
                        ".C",
                        ".c",
                    )
                )
            ]

            cfiles.extend(source_c_files)
        filecount = len(cfiles)
        self.code_cache.search_set.extend(cfiles)
        self.code_cache.process_files()
        self.code_cache.output(starttime=self.starttime, filecount=filecount)


def main(arg_s=None):
    """Parse arguments, drive program."""
    # this is where the command line interface we interact with is defined.
    # help is what gets displayed if the -h argument is passed
    # defaults can be specified. action="store_true" means that the option
    # defaults to false, and the argument's presence makes it true. For example
    # walking through directories recursively is disabled by default. When the
    # -r is present, recursive is True (turned on)
    starttime = datetime.now()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        help="print the ClonedCodeChecker's version and exit"
    )
    parser.add_argument(
        "-p",
        "--purgefilecache",
        action="store_true",
        help="Purge the filecache (found at $HOME/.filecache)"
    )
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="{}{}".format(
            "Search for duplicate code in given ",
            "directory and any sub-directories (recursive)"
        )
    )
    parser.add_argument(
        "-d",
        "--directory",
        default="./",
        help="{}{}".format(
            "Search for duplicate code in given ",
            "directory (but not sub-directories)",
        )
    )
    parser.add_argument("-j", action="store_true", help=argparse.SUPPRESS)

    args = parser.parse_args(arg_s)

    output_location = os.path.join(os.getcwd(), "report.txt")

    filecache_location = os.path.join(os.path.expanduser("~"), ".filecache")

    try:
        os.mkdir(filecache_location)
    except FileExistsError:
        pass

    if args.version:
        print("ClonedCodeChecker {}".format(version))
        return

    if args.j:
        output_location = os.path.join(args.directory, "report.txt")

    ccc = ClonedCodeChecker(
        output_location=output_location,
        filecache_location=filecache_location,
        starttime=starttime,
    )
    #########################################################################
    ccc.code_cache.filecache = filecache_location
    ccc.code_cache.output_dir = output_location
    #########################################################################
    if args.purgefilecache:
        ccc.code_cache.purge()

    if args.recursive:
        ccc.recursive_walk(directory=args.directory)
    else:
        ccc.load_cpp_files(args.directory)


# This is the entry point.
# It means "if this file was run from the command line, do this stuff
def run():
    """Only useful for testing. Program's entry point is main. See setup.py."""
    if __name__ == "__main__":
        # code_cache is the 'container' object. It holds cppFile objects
        # I create it here so every function above has access to it.
        sys.exit(main(arg_s=sys.argv[1:]))


run()
