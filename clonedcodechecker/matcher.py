"""The Matcher class owns all things involved in defining duplicate code.

This is where the tokenizer lives, and where matches across files are stored.
"""

import re


class Matcher:
    """
    The Matcher class.

    Slots:
    line_matches: A dictionary where the key is the line being matched,
    and the value is a list of filenames that contain the line.
    tox_regex: A compiled regular expression object. Not yet in use
    total_lineset: the set of all lines that have been seen by the matcher.
    """

    __slots__ = ["line_matches", "tok_regex", "total_lineset"]

    def __init__(self):
        """Build regular expression (tokenizer) object."""
        self.line_matches = {}
        self.total_lineset = set()

        number = '[0-9]+[.]?[0-9]*'      # Integer or decimal number
        assign = '='                     # Assignment operator
        e_n_d = ';'                        # Statement terminator
        i_d = '[A-Za-z_]+'                # Identifiers
        o_p = '[+]|[-]|(?<!/)[*](?!/)|(?<!/)/(?!/)'  # Arithmetic operators
        whitespace = r'[\s]+'               # spaces, tabs, and newlines
        mismatch = '.'                   # Any other character

        token_specification = [
            ('NUMBER', number),
            ('ASSIGN', assign),
            ('END', e_n_d),
            ('ID', i_d),
            ('OP', o_p),
            ('WHITESPACE', whitespace),
            ('MISMATCH', mismatch)
            ]
        t_string = '|'.join(('(?P<{}>{})'.format(pair[0], pair[1])
                             for pair in token_specification))
        self.tok_regex = re.compile(t_string)

    def print_matches(self, code):
        """Test the tokenizer."""
        for token in self.tok_regex.finditer(code):
            print(token.lastgroup, end=' ')
            input(token.group())

    def match_lines(self, fname, lineset):
        """Tracks what files have what lines.

        Take a set of lines from a file and the file's name,
        add the lines to line_matches.
        """
        for line in lineset.difference(self.total_lineset):
            self.line_matches[line] = [fname]
        for line in lineset.intersection(self.total_lineset):
            self.line_matches[line].append(fname)
        self.total_lineset = self.total_lineset.union(lineset)

    def show_multiple(self, outfile):
        """Print the line_matches dictionary to outfile."""
        print(outfile)
        with open(outfile, "w") as file:
            for k in self.line_matches:
                if len(self.line_matches[k]) > 1:
                    print(k, file=file)
                    print(self.line_matches[k], file=file)
                    # input(self.line_matches[k])
