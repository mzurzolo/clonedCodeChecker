"""Parse arguments, drive program."""

import os
import argparse
from .clonedcodechecker import ClonedCodeChecker


def main():
    """Parse arguments, drive program."""
    output_location = os.path.join(os.getcwd(), "report.txt")
    filecache_location = os.path.join(os.path.expanduser("~"), ".filecache")
    try:
        os.mkdir(filecache_location)
    except FileExistsError:
        pass
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

    args = parser.parse_args()

    ccc = ClonedCodeChecker()
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
    main()
