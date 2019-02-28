#!/usr/bin/env python3


import argparse
import os
# the next three imports allow us to use code from _common.py, cppFile.py, and
# codeCache.py
import _common as common
import cppFile as cpf
import codeCache as cC
import re


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
        # if the file has a .h extension and is visible:
        if f.endswith(".h") and not f.startswith("."):
            # add it to the codecache (process it)
            codecache.addFile(common.abspath(directory + f))


def recursive_walk(directory="."):
    # this iterates through every subdirectory, starting at whatever 'directory'
    # is. "for current, _folders, files" just gives us access to the folders
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

# Testing matches. eventually the matcher will be a tokenizer
def recursive_walk_testm(directory="."):
    token_specification = [
        ('NUMBER',   r'\d+(\.\d*)?'),  # Integer or decimal number
        ('ASSIGN',   r':='),           # Assignment operator
        ('END',      r';'),            # Statement terminator
        ('ID',       r'[A-Za-z]+'),    # Identifiers
        ('OP',       r'[+\-*/]'),      # Arithmetic operators
        ('NEWLINE',  r'\n'),           # Line endings
        ('SKIP',     r'[ \t]+'),       # Skip over spaces and tabs
        ('MISMATCH', r'.'),            # Any other character
    ]
    token_specification2 = [
    ('NUMBER',   '[0-9]+[.]?[0-9]*'),  # Integer or decimal number
    ('ASSIGN',   '='),           # Assignment operator
    ('END',      ';'),            # Statement terminator
    ('ID',       '[A-Za-z_]+'),    # Identifiers
    ('OP',       '[[+][-][*][/]]'),      # Arithmetic operators
    ('NEWLINE',  '[\n]'),           # Line endings
    ('WHITESPACE',     '[[ ][\t]]+'),       # Skip over spaces and tabs
    ('MISMATCH', '.'),            # Any other character
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    input(tok_regex)
    tok_regex2 = '|'.join(('(?P<{}>{})'.format(pair[0],pair[1]) for pair in token_specification2))
    input(tok_regex2)
    for current, _folders, files in os.walk(directory):
        if current[-1] is not "/":
            load_cpp_files(current+"/")
        else:
            load_cpp_files(current)
        codecache.testmatch()
        codecache.saveCache()

# this isn't doing anything useful. Debugging with print statements
def option_c():
    for file in os.listdir("./"):
        print(file)
        print(os.path.abspath(file))
        print("file only")
        common.parseFilename(file)
        print("os path abspath")
        common.parseFilename(os.path.abspath(file))

# main decides what functions to run based on the arguments in args.
# this is not complete
def main():

    # this is where the command line interface we interact with is defined.
    # help is what gets displayed if the -h argument is passed
    # defaults can be specified. action="store_true" means that the option
    # defaults to false, and the argument's presence makes it true. For example,
    # walking through directories recursively is disabled by default. When the
    # -r is present, recursive is True (turned on)
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', help="Purge C++ Code Cache",
                        action="store_true")
    parser.add_argument('-f', help="Search for duplicate code in given file")
    parser.add_argument('-o', help="Specify directory for the output file")
    parser.add_argument('-d', help="Search for duplicate code in given directory" +
                        "(but not sub-directories)", default="./")
    parser.add_argument('-c', help="Search for duplicate code in current" +
                        " directory (but not sub-directories)",
                        action="store_true")
    parser.add_argument('-r', help="Search for duplicate code recursively",
                        action="store_true")
    parser.add_argument('-m', help="Activate matcher", action="store_true")


    args = parser.parse_args()

    ###############################################################################

    if args.p:
        codecache.purge()

    if args.m:
        recursive_walk_testm(args.d)

    # If -f <filename> was not specified, args.f will be None, which will
    # evaluate false.
    if args.f:
        newFile = load_file(args.f)
        newFile.printSet()

    # Assumes that if -r was an argument, a directory was also specified
    # with -d. It doesn't check that that's actually what happened.
    if args.r:
        recursive_walk(args.d)
        #codecache.printCache()
        codecache.saveCache()
        codecache.scanSearchSet()


    if args.c:
        option_c()


# This is the entry point.
# It means "if this file was run from the command line, do this stuff
if __name__ == "__main__":
    # codecache is the 'container' object. It holds cppFile objects
    # I create it here so every function above has access to it.
    codecache = cC.codeCache()
    main()
