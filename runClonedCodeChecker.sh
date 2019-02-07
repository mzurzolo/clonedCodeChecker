#!/bin/sh

PROGRAM="Cloned Code Checker"
VERSION=0.0.1
AUTHOR="Mike Zurzolo <mikezurzolo@gmail.com>"

print_help()
{
  echo "$PROGRAM Version: $VERSION  Author: $AUTHOR"
  echo "Usage: "
  echo "./runClonedCodeChecker.sh [-a|-j|-c|-h] <parent_directory> [-R]"
  echo "Options: "
  echo "-a: whatever option a is"
  echo "-j: whatever option j is"
  echo "-c: whatever option c is"
  echo "-h: print this help message"
  echo "-R: run ClonedCodeChecker recursively, starting at <parent_directory>"
  echo "Defaults: "
  echo "<parent_directory> : current directory"
}

run_program()
{
  ./clonedCodeChecker.py #-a $arg_a -j $arg_j -c $arg_c -R $arg_R
}

while getopts ":ajcRh" opt; do
  case $opt in
    a) arg_a="$OPTARG"
    ;;
    j) arg_j="$OPTARG"
    ;;
    c) arg_c="$OPTARG"
    ;;
    h)
    print_help
    exit 0
    ;;
    R) arg_R="$OPTARG"
    ;;
    \?) echo "Invalid option -$OPTARG" >&2
    ;;
  esac
done

printf "Argument a is %s\n" "$arg_a"
printf "Argument j is %s\n" "$arg_j"
printf "Argument c is %s\n" "$arg_c"
printf "Argument R is %s\n" "$arg_R"
run_program
