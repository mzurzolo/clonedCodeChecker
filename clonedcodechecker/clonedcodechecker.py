"""cloned_code_checker is a static analysis tool for C/C++ Source Code."""

import os
from .codecache import CodeCache


class ClonedCodeChecker():
    """The ClonedCodeChecker collects files for its CodeCache."""

    def __init__(self):
        """Get new ClonedCodeChecker object."""
        self.code_cache = CodeCache()

    # "directory="." " means that directory is optional. If load_cpp_files is
    # not passed a directory, it uses ".", which is the current directory
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

        self.code_cache.process_files()
        self.code_cache.output()

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

        self.code_cache.process_files()
        self.code_cache.output()
