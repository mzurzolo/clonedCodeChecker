"""cloned_code_checker is a static analysis tool for C/C++ Source Code."""

import os
import sys
import argparse
from clonedcodechecker.codecache import CodeCache


class ClonedCodeChecker():
    """The ClonedCodeChecker collects files for its CodeCache."""

    def __init__(self, output_location=None, filecache_location=None):
        """Get new ClonedCodeChecker object."""
        self.code_cache = CodeCache()
        self.output_location = output_location
        self.filecache_location = filecache_location
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
            for file
            in os.scandir(directory)
            if file.is_file()
            and not file.name.startswith(".")]

        source_c_files = [
            file for file
            in absolute_files
            if any([file.endswith(".cpp"),
                    file.endswith(".c")])]

        self.code_cache.search_set.extend(source_c_files)
        self.code_cache.process_files()
        self.code_cache.output()

    def recursive_walk(self, directory="."):
        """Recursive directory walk."""
        cfiles = set()
        for current, _folders, files in os.walk(directory):
            absolute_files = [
                os.path.join(os.path.realpath(current), file)
                for file
                in files
                if not file.startswith(".")]

            source_c_files = [
                file for file
                in absolute_files
                if any([file.endswith(".cpp"),
                        file.endswith(".c")])]

            cfiles.update(source_c_files)

        self.code_cache.search_set.extend(cfiles)
        self.code_cache.process_files()
        self.code_cache.output()


def main(argS=sys.argv[1:]):
    """Parse arguments, drive program."""
    # this is where the command line interface we interact with is defined.
    # help is what gets displayed if the -h argument is passed
    # defaults can be specified. action="store_true" means that the option
    # defaults to false, and the argument's presence makes it true. For example
    # walking through directories recursively is disabled by default. When the
    # -r is present, recursive is True (turned on)
    parser = argparse.ArgumentParser()
    parser.add_argument('-p',
                        action="store_true",
                        help="Purge C++ Code Cache")
    parser.add_argument('-r',
                        action="store_true",
                        help="{}{}".format(
                            "Search for duplicate code in given ",
                            "directory and any sub-directories (recursive)"))
    parser.add_argument('-d',
                        default="./",
                        help="{}{}".format(
                            "Search for duplicate code in given ",
                            "directory (but not sub-directories)"))
    parser.add_argument('-t',
                        action="store_true",
                        help=argparse.SUPPRESS)

    args = parser.parse_args(argS)

    output_location = os.path.join(
        os.getcwd(),
        "report.txt")

    filecache_location = os.path.join(
        os.path.expanduser("~"),
        ".filecache")

    if args.t:
        output_location = "report.txt"
        filecache_location = ".filecache"

    try:
        os.mkdir(filecache_location)
    except FileExistsError:
        pass

    ccc = ClonedCodeChecker(output_location=output_location,
                            filecache_location=filecache_location)
    #########################################################################
    ccc.code_cache.filecache = filecache_location
    ccc.code_cache.output_dir = output_location
    ccc.code_cache.sync_cachedfiles()
    #########################################################################
    if args.p:
        ccc.code_cache.purge()

    if args.r:
        ccc.recursive_walk(directory=args.d)
    else:
        if args.d:
            ccc.load_cpp_files(args.d)


# This is the entry point.
# It means "if this file was run from the command line, do this stuff
if __name__ == "__main__":
    # code_cache is the 'container' object. It holds cppFile objects
    # I create it here so every function above has access to it.
    sys.exit(main(argS=sys.argv[1:]))
