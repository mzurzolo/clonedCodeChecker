#!/usr/bin/env python3

import argparse
import os
import _common as common
import cppFile as cpf
import codeCache as cC

parser = argparse.ArgumentParser()
parser.add_argument('-p', help="Purge C++ Code Cache")
parser.add_argument('-f', help="Search for duplicate code in given file")
parser.add_argument('-o', help="Specify directory for the output file")
parser.add_argument('-d', help="Search for duplicate code in given directory" +
                    "(but not sub-directories)", default="./")
parser.add_argument('-c', help="Search for duplicate code in current" +
                    " directory (but not sub-directories)",
                    action="store_true")
parser.add_argument('-r', help="Search for duplicate code recursively",
                    action="store_true")

###############################################################################
codecache = cC.codeCache()


def load_file(filename='example.txt'):
    return cpf.cppFile(os.path.abspath(filename))


def load_cpp_files(directory="."):
    for f in os.listdir(directory):
        if f.endswith(".cpp") and not f.startswith("."):
            codecache.addFile(os.path.abspath(directory + f))

        if f.endswith(".c") and not f.startswith("."):
            codecache.addFile(os.path.abspath(directory + f))


def recursive_walk(directory="."):
    for current, _folders, files in os.walk(directory, topdown=False):
        if current[-1] is not "/":
            load_cpp_files(current+"/")
        else:
            load_cpp_files(current)

        codecache.saveCache()


def option_c():
    for file in os.listdir("./"):
        print(file)
        print(os.path.abspath(file))
        print("file only")
        common.parseFilename(file)
        print("os path abspath")
        common.parseFilename(os.path.abspath(file))


def main(args):

    # If -f <filename> was not specified, args.f will be None, which will
    # evaluate false.
    if args.f:
        newFile = load_file(args.f)
        newFile.printSet()

    if args.r:
        recursive_walk(args.d)
        #codecache.printCache()
        codecache.saveCache()

    if args.c:
        option_c()



if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
