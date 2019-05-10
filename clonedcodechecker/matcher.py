"""The Matcher class owns all things involved in defining duplicate code.

This is where the tokenizer lives, where matches across files are stored,
and where the final output comes from.
"""

import re
from datetime import datetime
from collections import ChainMap, deque
import clonedcodechecker


class MergeUpdater(ChainMap):
    """Subclassed ChainMap with an altered update function."""

    def update(self, other):
        """Append instead of update. Use deques for fast appends."""
        for key in other:
            try:
                self[key].append(other[key])
            except KeyError:
                self[key] = deque()
                self[key].append(other[key])


class Matcher:
    """
    The Matcher class.

    Slots:
    total_linecount: The total lines analyzed
    mergeupdater: A modified ChainMap (dictionary) that updates the values of
        existing keys instead of overwriting them
    tox_regex: A dictionary of compiled regular expression objects that are
        used as 'filters' while processing strings of source code
    """

    def __init__(self):
        """Build a dictionary of compiled regular expressions.

        Get a MergeUpdater to track matches.
        Initialize total_linecount.
        """
        self.total_linecount = 0
        self.mergeupdater = MergeUpdater()

        token_spec = [
            (
                "FIRST_FILTER",
                r"""(?P<DOUBLE_SLASH_COMMENT>//.*?\n)|
                                 (?P<SLASH_STAR_COMMENT>/\*.*?\*/)|
                                 (?P<DOUBLEQUOTES>\".*?\")|
                                 (?P<SEMICOLONWS>;\s*)|
                                 (?P<TO_NEXT_BRACE>\s*\})|
                                 (?P<WHITESPACE>\s+)|
                                 (?P<NOTWHITESPACE>\w+\s*)|
                                 (?P<NONWORD>\W\s*)|
                                 (?P<FAILURE>.)
                                 """,
            ),
            (
                "COMMENT_FILTER",
                r"""(?P<DOUBLE_SLASH_COMMENT>//.*?\n)|
                             (?P<SLASH_STAR_COMMENT>/\*.*?\*/)
                             """,
            ),
            ("QUOTEFILTER", r"""(?P<DOUBLEQUOTES>\".*?\")"""),
            ("OPEN_BRACE", r"""(?P<OPEN_BRACE>\{)"""),
            ("CLOSE_BRACE", r"""(?P<CLOSE_BRACE>\})"""),
            ("PAREN_PAIR", r"""(?P<PAREN_PAIR>\)\s*?\{)"""),
            ("LINE_COUNTER", r"""\n"""),
        ]

        self.tok_regex = {}
        for pair in token_spec:
            self.tok_regex[pair[0]] = re.compile(pair[1], re.X | re.S)

    def tokenize(self, text, startline=1):
        """Process text.

        Return a list of 3-tuples (member, startline, endline).
        """
        member_accumulator = ""
        comment_filtered = ""
        member_list = deque()
        for token in self.tok_regex["FIRST_FILTER"].finditer(text):
            # Before we start building a member, drop things
            if member_accumulator == "":
                if any(
                    [
                        token.lastgroup == "DOUBLE_SLASH_COMMENT",
                        token.lastgroup == "SLASH_STAR_COMMENT",
                        token.lastgroup == "WHITESPACE",
                        token.lastgroup == "SEMICOLONWS",
                    ]
                ):
                    startline += len(
                        self.tok_regex["LINE_COUNTER"].findall(token.group())
                    )
                    continue
            # Accumulate tokens while building member
            member_accumulator += token.group()
            # Filter comments that may be inside the member (like this one)
            comment_filtered += re.sub(
                self.tok_regex["COMMENT_FILTER"], "", token.group()
            )
            # End on a brace
            if token.lastgroup == "TO_NEXT_BRACE":
                # Remove quotes (since they may contain braces)
                quote_filtered = re.sub(
                    self.tok_regex["QUOTEFILTER"], "", comment_filtered
                )
                # Count open and close braces
                open_count = len(
                    self.tok_regex["OPEN_BRACE"].findall(quote_filtered)
                )
                close_count = len(
                    self.tok_regex["CLOSE_BRACE"].findall(quote_filtered)
                )
                # If it ends with a close brace, this is maybe a member
                if open_count == close_count and quote_filtered.endswith("}"):
                    # Keep track of line count
                    startline_here = startline
                    startline += len(
                        self.tok_regex["LINE_COUNTER"].findall(
                            member_accumulator
                        )
                    )
                    # We want to start on the next line
                    endline = startline + 1
                    # Comment filtered is the member without comments
                    # Add member, start line, and end line as a 3-tuple to
                    #  the member_list
                    member_list.append(
                        (comment_filtered, startline_here, endline)
                    )
                    member_accumulator = ""
                    comment_filtered = ""
        # Catch last section of source code just in case
        if member_accumulator != "":
            if self.tok_regex["CLOSE_BRACE"].findall(comment_filtered):
                quote_filtered = re.sub(
                    self.tok_regex["QUOTEFILTER"], "", comment_filtered
                )
                open_count = len(
                    self.tok_regex["OPEN_BRACE"].findall(quote_filtered)
                )
                close_count = len(
                    self.tok_regex["CLOSE_BRACE"].findall(quote_filtered)
                )
                if open_count == close_count and close_count > 0:
                    startline_here = startline
                    startline += len(
                        self.tok_regex["LINE_COUNTER"].findall(
                            member_accumulator
                        )
                    )
                    endline = startline + 1
                    member_list.append(
                        (comment_filtered, startline_here, endline)
                    )
                    member_accumulator = ""
            # Needed for accurate line recording
            startline += len(
                self.tok_regex["LINE_COUNTER"].findall(member_accumulator)
            )
        # Output goes to codecache instead of passing directly to
        # match_tokens below.
        return (member_list, startline)

    def match_tokens(self, filename, member_tokens):
        """Loop through member tokens, adding to mergeupdater."""
        for token in member_tokens:
            # Only consider members that contain ) {
            # This filters members written as:   something()={}
            if self.tok_regex["PAREN_PAIR"].findall(token[0]):
                # Sending each token through seperately ensures duplicates in
                # the same file are found
                self.mergeupdater.update(
                    {token[0]: (filename, token[1], token[2])}
                )

    def print_output(self, outfile, starttime=None, filecount=None):
        """Print mergeupdater matches to outfile."""
        print(outfile)
        files_set = set()
        duplicate_count = 0
        with open(outfile, "w") as file:
            print("ClonedCodeChecker", file=file)
            print(
                "Version: {}".format(clonedcodechecker.__version__), file=file
            )
            print("Start time: {}".format(starttime), file=file)
            print("Run time: {}".format(datetime.now() - starttime), file=file)
            print("Files analyzed: {}".format(filecount), file=file)
            print(
                "Lines analyzed: {}\n".format(self.total_linecount), file=file
            )
            for key in self.mergeupdater.keys():
                if len(self.mergeupdater[key]) > 1:
                    print("Duplicate member found in: \n", file=file)
                    duplicate_count += 1
                    for val in self.mergeupdater[key]:
                        files_set.add(val[0])
                        print(
                            "\t",
                            "\t",
                            "\t",
                            "\t",
                            "\t",
                            "{} line: {}".format(val[0], val[1]),
                            file=file,
                        )
                    print("Member:         \n\n", key, file=file)
                    print("\n\n", file=file)
            print("Total duplicates: {}".format(duplicate_count), file=file)
            print("Files affected: {}".format(len(files_set)), file=file)

        print("ClonedCodeChecker")
        print("Version: {}".format(clonedcodechecker.__version__))
        print("Start time: {}".format(starttime))
        print("Run time: {}".format(datetime.now() - starttime))
        print("Files analyzed: {}".format(filecount))
        print("Lines analyzed: {}\n".format(self.total_linecount))
        print("Total duplicates: {}".format(duplicate_count))
        print("Files affected: {}".format(len(files_set)))
