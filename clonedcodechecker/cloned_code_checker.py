"""cloned_code_checker was designed to act as a static analysis tool for
C/C++ Source Code"""
import os
import argparse
import _common as common
import CodeCache as cC


# "directory="." " means that directory is optional. If load_cpp_files is not
# passed a directory, it uses ".", which is the current directory
def load_cpp_files(directory="."):
    """iterate through the list of files in directory, load them"""
    for file in os.listdir(directory):
        # filenames and folder names that begin with a . are hidden. We don't
        # want hidden files
        # if the file has a .cpp extension and is visible:
        if file.endswith(".cpp") and not file.startswith("."):
            # add it to the CODE_CACHE (process it)
            CODE_CACHE.addFile(common.abspath(directory + file))
            # if the file has a .c extension and is visible:
        if file.endswith(".c") and not file.startswith("."):
            # add it to the CODE_CACHE (process it)
            CODE_CACHE.addFile(common.abspath(directory + file))
        # if the file has a .h extension and is visible:
        if file.endswith(".h") and not file.startswith("."):
            # add it to the CODE_CACHE (process it)
            CODE_CACHE.addFile(common.abspath(directory + file))


def recursive_walk(directory="."):
    """this iterates through every subdirectory, starting at 'directory'
    for processing by the clonedcodechecker"""
    for current, _folders, files in os.walk(directory):
        # current is a string. [-1] is negative-indexing. it means "the last"
        # element in current
        if current[-1] != "/":
            load_cpp_files(current+"/")
        else:
            load_cpp_files(current)
        # savecache clears files out of memory. We have to think through how
        # we decide whether a file should be in memory, or saved off to the
        # filecache.
        CODE_CACHE.saveCache()


# Testing matches. eventually the matcher will be a tokenizer
def recursive_walk_testm(directory="."):
    """test function"""
    for current, _folders in os.walk(directory):
        if current[-1] != "/":
            load_cpp_files(current+"/")
        else:
            load_cpp_files(current)
        CODE_CACHE.testmatch()
        CODE_CACHE.saveCache()


def main():
    """Parse arguments supplied by user,
     drive program based on those arguments"""
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
        recursive_walk(args.d)
        CODE_CACHE.saveCache()
        CODE_CACHE.output()
    else:
        load_cpp_files(args.d)


# This is the entry point.
# It means "if this file was run from the command line, do this stuff
if __name__ == "__main__":
    # CODE_CACHE is the 'container' object. It holds cppFile objects
    # I create it here so every function above has access to it.
    CODE_CACHE = cC.CodeCache()
    main()
