#!/usr/bin/env python3

import argparse
import os
import pandas as pd
from cppFile import cppFile


parser = argparse.ArgumentParser()
parser.add_argument('-p', help="Purge C++ Code Cache")
parser.add_argument('-f', help="Search for duplicate code in given file")
parser.add_argument('-o', help="Specify directory for the output file")
parser.add_argument('-d', help="Search for duplicate code in given directory \
                    (but not sub-directories)", default="./")
parser.add_argument('-c', help="Search for duplicate code in current directory \
                    (but not sub-directories)",
                    action="store_true")
parser.add_argument('-r', help="Search for duplicate code recursively",
                    action="store_true")



def load_file(filename='example.txt'):
    newFile = cppFile(filename)
    with open(filename,'r') as file:
        for line in file:
            newFile.addLine( line.strip() )

    return newFile


def recursive_walk(directory="./"):
    for current, _folders, files in os.walk(directory):
        print(current)
        map(lambda x: print("___{}".format(x)), _folders)
        map(lambda x: print("___...___{}".format(x)), files)


def option_c():
    for file in os.listdir("./"):
        print(file)


def main(args):

    # If -f <filename> was not specified, args.f will be None, which will
    # evaluate false.
    if args.f:
        newFile = load_file(args.f)
        newFile.printSet()


    if args.r:
        recursive_walk(args.d)

    if args.c:
        option_c()



if __name__ == "__main__":
    args = parser.parse_args()
    main(args)
