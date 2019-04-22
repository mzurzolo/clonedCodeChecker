"""The Matcher class owns all things involved in defining duplicate code.

This is where the tokenizer lives, and where matches across files are stored.
"""

import re
from datetime import datetime
from collections import ChainMap, deque


class MergeUpdater(ChainMap):
    """Subclassed ChainMap with an altered update function."""

    def update(self, other):
        """Update appends instead of replacing."""
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
    line_matches: A dictionary where the key is the line being matched,
    and the value is a list of filenames that contain the line.
    tox_regex: A compiled regular expression object. Not yet in use
    total_lineset: the set of all lines that have been seen by the matcher.
    """

    def __init__(self):
        """Build regular expression (tokenizer) object."""
        self.line_matches = {}
        self.total_lineset = set()
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
            ("MEMBER", r"""(?P<MEMBER>(\S+\s*)+?\S+\s*\(.*?\)\s*?\{.*?\})"""),
        ]

        self.tok_regex = {}
        for pair in token_spec:
            self.tok_regex[pair[0]] = re.compile(pair[1], re.X | re.S)

    def tokenize(self, text, startline=1):
        """Yield tuples of text and line position for every found match."""
        member_accumulator = ""
        comment_filtered = ""
        member_list = deque()
        for token in self.tok_regex["FIRST_FILTER"].finditer(text):
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

            member_accumulator += token.group()
            comment_filtered += re.sub(
                self.tok_regex["COMMENT_FILTER"], "", token.group()
            )
            if token.lastgroup == "TO_NEXT_BRACE":
                quote_filtered = re.sub(
                    self.tok_regex["QUOTEFILTER"], "", comment_filtered
                )
                open_count = len(
                    self.tok_regex["OPEN_BRACE"].findall(quote_filtered)
                )
                close_count = len(
                    self.tok_regex["CLOSE_BRACE"].findall(quote_filtered)
                )
                if open_count == close_count and quote_filtered.endswith("}"):
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
                    comment_filtered = ""

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
                if open_count == close_count and quote_filtered.endswith("}"):
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

            startline += len(
                self.tok_regex["LINE_COUNTER"].findall(member_accumulator)
            )

        return (member_list, startline)

    def match_tokens(self, filename, member_tokens):
        """Test the token matcher."""
        for token in member_tokens:
            if self.tok_regex["PAREN_PAIR"].findall(token[0]):
                self.mergeupdater.update({token[0]: (filename, token[1], token[2])})

    def print_output(self, outfile, starttime=None, filecount=None):
        """Print the line_matches dictionary to outfile."""
        print(outfile)
        with open(outfile, "w") as file:
            print("ClonedCodeChecker", file=file)
            print("Version: 0.0.1", file=file)
            print("Start time: {}".format(starttime), file=file)
            print("Run time: {}".format(datetime.now() - starttime), file=file)
            print("Files analyzed: {}".format(filecount), file=file)
            print(
                "Lines analyzed: {}\n".format(self.total_linecount), file=file
            )
            for key in self.mergeupdater.keys():
                if len(self.mergeupdater[key]) > 1:
                    print("Duplicate member found in: \n", file=file)
                    for val in self.mergeupdater[key]:
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

        print("ClonedCodeChecker")
        print("Version: 0.0.1")
        print("Start time: {}".format(starttime))
        print("Run time: {}".format(datetime.now() - starttime))
        print("Files analyzed: {}".format(filecount))
        print("Lines analyzed: {}\n".format(self.total_linecount))
