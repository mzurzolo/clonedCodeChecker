#!/usr/bin/env python3

import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-a', help="a?")
parser.add_argument('-j', help="j?")
parser.add_argument('-c', help="c?")
parser.add_argument('-R', help="R?")

args = parser.parse_args()
arg_a = args.a
arg_j = args.j
arg_c = args.c
arg_R = args.R

def load_file(filename='example.txt'):
    lineslist = []
    with open(filename,'r') as file:
        for line in file:
            lineslist.append( line.strip() )

    return lineslist


def main(arg_a=None, arg_j=None, arg_c=None, arg_R=None):

    lineslist = load_file()
    # looping examples? not sure what examples to include... will add more
    for line in lineslist:
        print(line)

    for i in range(len(lineslist)):
        if len(lineslist[i]) == 0:
            continue
        for split in lineslist[i].split():
            print(split.strip(), end=' ')
        print()




if __name__ == "__main__":
    main()
