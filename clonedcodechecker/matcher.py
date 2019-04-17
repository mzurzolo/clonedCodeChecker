"""The Matcher class owns all things involved in defining duplicate code.

This is where the tokenizer lives, and where matches across files are stored.
"""

import re
from collections import namedtuple, ChainMap, deque

Token = namedtuple("Token", ["token", "value", "span", "line"])


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

    __slots__ = ["line_matches", "tok_regex", "total_lineset", "mergeupdater"]

    def __init__(self):
        """Build regular expression (tokenizer) object."""
        self.line_matches = {}
        self.total_lineset = set()
        self.mergeupdater = MergeUpdater()

        token_spec = [
            (
                "FIRST_FILTER",
                r"""(?P<DOUBLE_SLASH_COMMENT>//.*?\n)|
                                 (?P<SLASH_STAR_COMMENT>/\*.*?\*/)|
                                 (?P<PREPROCESSOR>\#.*?\n)|
                                 (?P<WHITESPACE>\s+)|
                                 (?P<SEMICOLONWS>;\s*)|
                                 (?P<TO_NEXT_BRACE>.*?\})|
                                 (?P<NOTWHITESPACE>\S+\s+)
                                 """,
            ),
            ("OPEN_BRACE", r"""(?P<OPEN_BRACE>\{)"""),
            ("CLOSE_BRACE", r"""(?P<CLOSE_BRACE>\})"""),
            ("PAREN_PAIR", r"""(?P<PAREN_PAIR>\)\s*?\{)"""),
            ("LINE_COUNTER", r"""\n"""),
            ("MEMBER", r"""(?P<MEMBER>(\S+\s*)+?\S+\s*\(.*?\)\s*?\{.*?\})"""),
        ]

        self.tok_regex = {}
        for pair in token_spec:
            self.tok_regex[pair[0]] = re.compile(pair[1], re.X | re.S)

    def tokenize(self, text):
        """Yield tuples of text and line position for every found match."""
        lines = 1
        member_accumulator = ""
        member_list = []
        for token in self.tok_regex["FIRST_FILTER"].finditer(text):

            if token.lastgroup == "DOUBLE_SLASH_COMMENT":
                if member_accumulator == "":
                    lines += len(
                        self.tok_regex["LINE_COUNTER"].findall(token.group())
                    )
                    continue

            if token.lastgroup == "SLASH_STAR_COMMENT":
                if member_accumulator == "":
                    lines += len(
                        self.tok_regex["LINE_COUNTER"].findall(token.group())
                    )
                    continue

            if token.lastgroup == "PREPROCESSOR":
                if member_accumulator == "":
                    lines += len(
                        self.tok_regex["LINE_COUNTER"].findall(token.group())
                    )
                    continue

            if token.lastgroup == "WHITESPACE":
                if member_accumulator == "":
                    lines += len(
                        self.tok_regex["LINE_COUNTER"].findall(token.group())
                    )
                    continue

            if token.lastgroup == "SEMICOLONWS":
                #input(token.group())
                if member_accumulator == "":
                    lines += len(
                        self.tok_regex["LINE_COUNTER"].findall(token.group())
                    )
                    continue

            member_accumulator += token.group()
            if token.lastgroup == "TO_NEXT_BRACE":
                if self.tok_regex["PAREN_PAIR"].findall(member_accumulator):
                    open_count = len(
                        self.tok_regex["OPEN_BRACE"].findall(member_accumulator)
                    )
                    close_count = len(
                        self.tok_regex["CLOSE_BRACE"].findall(member_accumulator)
                    )
                    if open_count == close_count:
                        startline = lines
                        lines += len(
                            self.tok_regex["LINE_COUNTER"].findall(
                                member_accumulator
                            )
                        )
                        endline = lines
                        member_list.append((member_accumulator, startline, endline))
                        member_accumulator = ""

        if member_accumulator != "":
            if self.tok_regex["CLOSE_BRACE"].findall(member_accumulator):
                if self.tok_regex["PAREN_PAIR"].findall(member_accumulator):
                    open_count = len(
                        self.tok_regex["OPEN_BRACE"].findall(member_accumulator)
                    )
                    close_count = len(
                        self.tok_regex["CLOSE_BRACE"].findall(member_accumulator)
                    )
                    if open_count == close_count:
                        startline = lines
                        lines += len(
                            self.tok_regex["LINE_COUNTER"].findall(
                                member_accumulator
                            )
                        )
                        endline = lines + 1
                        member_list.append((member_accumulator, startline, endline))
                        member_accumulator = ""

            lines += len(
                self.tok_regex["LINE_COUNTER"].findall(member_accumulator)
            )

        return (member_list, lines)

    def match_tokens(self, filename, member_tokens):
        """Test the token matcher."""
        for token in member_tokens:
            self.mergeupdater.update({token[0]: (filename, token[1], token[2])})

    def print_output(self, outfile):
        """Print the line_matches dictionary to outfile."""
        print(outfile)
        with open(outfile, "w") as file:
            for key in self.mergeupdater.keys():
                if len(self.mergeupdater[key]) > 1:
                    print("Duplicate member found in: \n", file=file)
                    for val in self.mergeupdater[key]:
                        print("\t", "\t", "\t", "\t", "\t", val, file=file)
                    print("Member:         \n\n", key, file=file)
                    print("\n\n", file=file)
