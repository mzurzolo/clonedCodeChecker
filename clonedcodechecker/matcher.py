"""The Matcher class owns all things involved in defining duplicate code.

This is where the tokenizer lives, and where matches across files are stored.
"""

import re
from collections import namedtuple, ChainMap, deque
from _collections_abc import Mapping

Token = namedtuple("Token", ['token', 'value', 'span', 'line'])


class MergeUpdater(ChainMap):
    """Subclassed ChainMap with an altered update function."""

    def update(self, other):
        """Update appends instead of replacing."""
        if isinstance(other, Mapping):
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

        double_slash_comment = r'//.*?\n'      # comment up to newline
        slash_star_comment = r'/\*.*?\*/'       # comment open to close
        # Containers (more)
        brace_c = r'\{.*?\}'
        #bracket_c = r'\[.*?\]'
        #paren_c = r'\(.*?\)'
        newline = r'\n'
        other = r'.*?\n'
        token_specification = [
            ('DOUBLE_SLASH_COMMENT', double_slash_comment),  # Comments
            ('SLASH_STAR_COMMENT', slash_star_comment),
            ('BRACE_C', brace_c),
            #('BRACKET_C', bracket_c),
            #('PAREN_C', paren_c),
            ('NEWLINE', newline),
            ('OTHER', other)
        ]
        t_string = '|'.join(('(?P<{}>{})'.format(pair[0], pair[1])
                             for pair in token_specification))
        self.tok_regex = re.compile(t_string, re.S | re.A)

    def tokenize(self, text):
        """Yield 4-tuples for every found match."""
        linecount = 0
        for token in self.tok_regex.finditer(text):
            if token.lastgroup == 'NEWLINE':
                linecount += 1
            elif token.lastgroup == 'OTHER':
                linecount += 1
            else:
                pass
            if token.lastgroup == 'SLASH_STAR_COMMENT':
                linecount += len(token.group().split("\n"))
            if all(
                    [
                        token.lastgroup != 'DOUBLE_SLASH_COMMENT',
                        token.lastgroup != 'SLASH_STAR_COMMENT',
                        token.lastgroup != 'NEWLINE',
                        token.lastgroup == 'BRACE_C'
                    ]):
                yield Token(
                    token.lastgroup,
                    token.group(),
                    token.span(),
                    linecount)

    def get_tokens(self, text):
        """Return a list of all tokens in the text."""
        return [token for token in self.tokenize(text)]

    def match_tokens(self, file):
        """Test the token matcher."""
        all_tokens = [tok.value for tok
                      in self.get_tokens(file.linestring)]
        new_dict = dict(
            zip(set(all_tokens),
                [file.filename] * len(set(file.all_lines)))
        )

        self.mergeupdater.update(new_dict)

    def print_output(self, outfile):
        """Print the line_matches dictionary to outfile."""
        print(outfile)
        with open(outfile, "w") as file:
            for key in self.mergeupdater.keys():
                if len(self.mergeupdater[key]) > 1:
                    print('line:         ', key, file=file)
                    print("was found in: ", file=file)
                    for val in self.mergeupdater[key]:
                        print('\t', '\t', '\t', val, file=file)
                    print('', file=file)
