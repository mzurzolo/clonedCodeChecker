"""cloned_code_checker is a static analysis tool for C/C++ Source Code."""

import os
import argparse
from threading import Thread
from clonedcodechecker.code_cache import CodeCache


class ClonedCodeChecker():

    def __init__(self):
        self.code_cache = CodeCache()

    # "directory="." " means that directory is optional. If load_cpp_files is not
    # passed a directory, it uses ".", which is the current directory
    def load_cpp_files(self, directory="."):
        """Iterate through the list of files in directory, load them."""
        absolute_files = [
            os.path.realpath(file.path)
            for file
            in os.scandir(directory)
            if file.is_file()
            and not file.name.startswith(".")]

        source_h_files = [
            file for file
            in absolute_files
            if any([file.endswith(".hpp"),
                    file.endswith(".h")])]

        source_c_files = [
            file for file
            in absolute_files
            if any([file.endswith(".cpp"),
                    file.endswith(".c")])]

        self.code_cache.search_set.extend(source_c_files)
        self.code_cache.search_set.extend(source_h_files)

        adder_thread = Thread(target=self.code_cache.thread_add)
        saver_thread = Thread(target=self.code_cache.thread_save)
        adder_thread.start()
        saver_thread.start()


    def recursive_walk(self, directory="."):
        """Recursive directory walk."""
        hfiles = set()
        cfiles = set()
        for current, _folders, files in os.walk(directory):
            absolute_files = [
                os.path.join(os.path.realpath(current), file)
                for file
                in files
                if not file.startswith(".")]

            source_h_files = [
                file for file
                in absolute_files
                if any([file.endswith(".hpp"),
                        file.endswith(".h")])]

            source_c_files = [
                file for file
                in absolute_files
                if any([file.endswith(".cpp"),
                        file.endswith(".c")])]

            hfiles.update(source_h_files)
            cfiles.update(source_c_files)

        self.code_cache.search_set.extend(cfiles)
        self.code_cache.search_set.extend(hfiles)

        adder_thread = Thread(target=self.code_cache.thread_add)
        saver_thread = Thread(target=self.code_cache.thread_save)
        adder_thread.start()
        saver_thread.start()


    def main(self, args=None):

        #########################################################################
        self.code_cache.filecache = args.e + "/.filecache/"
        self.code_cache.output_dir = "{}/report.txt".format(args.o)
        self.code_cache.sync_cachedfiles()
        #########################################################################
        if args.p:
            self.code_cache.purge()

        if args.r:
            self.recursive_walk(directory=args.d)
        else:
            if args.d:
                self.load_cpp_files(args.d)


# This is the entry point.
# It means "if this file was run from the command line, do this stuff
if __name__ == "__main__":
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

    args = parser.parse_args()
    # code_cache is the 'container' object. It holds cppFile objects
    # I create it here so every function above has access to it.
    ccc = ClonedCodeChecker()
    ccc.main(args)
