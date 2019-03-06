import argparse
import os
import _common as common
import codeCache as cC


# "directory="." " means that directory is optional. If load_cpp_files is not
# passed a directory, it uses ".", which is the current directory
def load_cpp_files(directory="."):
    # iterate through the list of files in the current directory
    for f in os.listdir(directory):
        # filenames and folder names that begin with a . are hidden. We don't
        # want hidden files
        # if the file has a .cpp extension and is visible:
        if f.endswith(".cpp") and not f.startswith("."):
            # add it to the codecache (process it)
            codecache.addFile(common.abspath(directory + f))
        # if the file has a .c extension and is visible:
        if f.endswith(".c") and not f.startswith("."):
            # add it to the codecache (process it)
            codecache.addFile(common.abspath(directory + f))


def recursive_walk(directory="."):
    # this iterates through every subdirectory, starting at 'directory'
    # "for current, _folders, files" just gives us access to the folders
    # and files. it doesn't nest iterations. (if there's one sub-directory with
    # 1000 files, the loop doesn't run 1000 times)
    for current, _folders, files in os.walk(directory):
        # current is a string. [-1] is negative-indexing. it means "the last"
        # element in current
        if current[-1] is not "/":
            load_cpp_files(current+"/")
        else:
            load_cpp_files(current)
        # savecache clears files out of memory. We have to think through how
        # we decide whether a file should be in memory, or saved off to the
        # filecache.
        codecache.saveCache()


def main():

    # this is where the command line interface we interact with is defined.
    # help is what gets displayed if the -h argument is passed
    # defaults can be specified. action="store_true" menas that the option
    # defaults to false, and the argument's presence makes it true. For example
    # walking through directories recursively is disabled by default. When the
    # -r is present, recursive is True (turned on)
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', help="Purge C++ Code Cache",
                        action="store_true")
    # parser.add_argument('-f', help="Search for duplicate code in given file")
    parser.add_argument('-o', help="Specify directory for the output file",
                        default="./report.txt")
    parser.add_argument('-e', help=argparse.SUPPRESS)
    parser.add_argument('-r', help="Search for duplicate code in given " +
                        "directory and any sub-directories (recursive)",
                        action="store_true")
    parser.add_argument('-d', help="Search for duplicate code in given " +
                        "directory (but not sub-directories)", default="./")

    args = parser.parse_args()

    #########################################################################
    codecache.filecache = args.e + "./filecache/"
    codecache.sync_cachedfiles()
    #########################################################################

    if args.p:
        codecache.purge()

    if args.r:
        recursive_walk(args.d)
        codecache.saveCache()
    else:
        load_cpp_files(args.d)


# This is the entry point.
# It means "if this file was run from the command line, do this stuff
if __name__ == "__main__":
    # codecache is the 'container' object. It holds cppFile objects
    # I create it here so every function above has access to it.
    codecache = cC.codeCache()
    main()
