"""cloned_code_checker is a static analysis tool for C/C++ Source Code."""

import os
import argparse
from code_cache import CodeCache


# "directory="." " means that directory is optional. If load_cpp_files is not
# passed a directory, it uses ".", which is the current directory
def load_cpp_files(directory="."):
    """Iterate through the list of files in directory, load them."""
    absolute_files = [
        os.path.realpath(file.path)
        for file
        in os.scandir(directory)
        if file.is_file()
        and not file.name.startswith(".")]
    source_files = [
        file for file
        in absolute_files
        if any([file.endswith(".cpp"),
                file.endswith(".c"),
                file.endswith(".h")])]

    for file in source_files:
        # add it to the CODE_CACHE (process it)
        CODE_CACHE.add_file(file)


def recursive_walk(directory="."):
    """Recursive directory walk."""
    for current, _folders, files in os.walk(directory):
        # current is a string. [-1] is negative-indexing. it means "the last"
        # element in current
        absolute_files = [
            os.path.join(os.path.realpath(current), file)
            for file
            in files
            if not file.startswith(".")]
        source_files = [
            file for file
            in absolute_files
            if any([file.endswith(".cpp"),
                    file.endswith(".c"),
                    file.endswith(".h")])]

        for file in source_files:
            # add it to the CODE_CACHE (process it)
            CODE_CACHE.add_file(file)
        CODE_CACHE.save_cache()


# Testing matches. eventually the matcher will be a tokenizer
def recursive_walk_testm(directory="."):
    """Test function."""
    for current, _folders in os.walk(directory):
        if current[-1] != "/":
            load_cpp_files(current+"/")
        else:
            load_cpp_files(current)
        CODE_CACHE.testmatch()
        CODE_CACHE.save_cache()


def main():
    """Parse arguments, drive program."""
    # this is where the command line interface we interact with is defined.
    # help is what gets displayed if the -h argument is passed
    # defaults can be specified. action="store_true" means that the option
    # defaults to false, and the argument's presence makes it true. For example
    # walking through directories recursively is disabled by default. When the
    # -r is present, recursive is True (turned on)
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', help=argparse.SUPPRESS)
    parser.add_argument('-e', help=argparse.SUPPRESS)
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
    parser.add_argument('-m',
                        action="store_true",
                        help="Activate matcher")

    args = parser.parse_args()
    #########################################################################
    CODE_CACHE.filecache = args.e + "/.filecache/"
    CODE_CACHE.sync_cachedfiles()
    #########################################################################

    if args.p:
        CODE_CACHE.purge()

    if args.m:
        recursive_walk_testm(args.d)

    if args.r:
        recursive_walk(directory=args.d)
        CODE_CACHE.save_cache()
        CODE_CACHE.output("{}/report.txt".format(args.o))
    else:
        load_cpp_files(args.d)


# This is the entry point.
# It means "if this file was run from the command line, do this stuff
if __name__ == "__main__":
    # CODE_CACHE is the 'container' object. It holds cppFile objects
    # I create it here so every function above has access to it.
    CODE_CACHE = CodeCache()
    main()
