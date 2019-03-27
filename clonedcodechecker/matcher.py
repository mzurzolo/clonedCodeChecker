"""The Matcher class owns all things involved in defining duplicate code.

This is where the tokenizer lives, and where matches across files are stored.
"""

import re
from collections import namedtuple

Token = namedtuple("Token", ['token', 'value', 'span'])

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

        # Comments
        double_slash_comment = r'//.*?\n'      # comment up to newline
        slash_star_comment = r'/\*.*?\*/'       # comment open to close
        # Preprocessor
        include = r'#[/s]*?include.*?\n'
        define = r'#[/s]*?define.*?\n'
        ifdef = r'#ifdef.*?\n'
        endif = r'#[\s]*?endif.*?\n'
        undef = r'#[/s]*?undef.*?\n'
        # Containers
        brace = r'[\{\}]'
        bracket = r'[\[\]]'
        paren = r'[()]'
        # Operators
        arithmetic_op = r'\/|\*|\-|\+|\%|\+\+|\-\-'
        # readable: [/,*,-,+,%,++,--]
        relational_op = r'\=\=|\!\=|\<[=]|\>[=]|\<|\>'
        # readable: [==,!=,<,<=,>,>=]
        logical_op = r'&&|\|\||\!'
        # readable: [&&,||,!]
        bitwise_op = r'&|\||\^|\~|\<\<|\>\>'
        # readable: [&,|,^,~,<<,>>]
        arithmetic_and_assign = r'\+\=|\-\=|\*\=|\/\=|\%\='
        # readable: [+=,-=,*=,/=,%=]
        bitwise_and_assign = r'\<\<\=|\>\>\=|\&\=|\^\=|\|\='
        # readable: [<<=,>>=,&=,^=,|=]
        # Specials
        scope_resolution = r'\:\:'
        addr_of = r'&[A-Za-z_]+'
        pass_by_ref = r'[A-Za-z_]+&'
        pointer = r'\*[A-Za-z_]+|\-\>'
        conditional = r'\?\:'
        dot = r'[.]'
        # Other
        assign = r'='
        sep = ','
        e_n_d = r';'
        at_symbol = r'@'
        single_colon = r':'
        question_mark = r'\?'
        dollar_sign = r'\$'
        pound = r'#'
        quote = r'\"|\'|\`'
        backslash = r'\\'
        # Unicode
        cp_right = u'\N{COPYRIGHT SIGN}'
        empty_set = u'\N{LATIN CAPITAL LETTER O WITH STROKE}'
        empty_set_lc = u'\N{LATIN SMALL LETTER O WITH STROKE}'
        b_sharp = u'\N{LATIN CAPITAL LETTER SHARP S}'
        b_sharp_lc = u'\N{LATIN SMALL LETTER SHARP S}'
        # Regular
        number = r'[0-9]+?'
        i_d = r'[A-Za-z_]+'
        whitespace = r'[\s]+'
        # Trash
        mismatch = '.'

        token_specification = [
            ('DOUBLE_SLASH_COMMENT', double_slash_comment),  # Comments
            ('SLASH_STAR_COMMENT', slash_star_comment),
            ('INCLUDE', include),                            # Preprocessor
            ('DEFINE', define),
            ('IFDEF', ifdef),
            ('ENDIF', endif),
            ('UNDEF', undef),
            ('BRACE', brace),                                # Containers
            ('BRACKET', bracket),
            ('PAREN', paren),
            ('RELATIONAL_OP', relational_op),                # Operators
            ('LOGICAL_OP', logical_op),
            ('BITWISE_OP', bitwise_op),
            ('ARITHMETIC_AND_ASSIGN', arithmetic_and_assign),
            ('BITWISE_AND_ASSIGN', bitwise_and_assign),
            ('SCOPE_RESOLUTION', scope_resolution),         # Specials
            ('ADDR_OF', addr_of),
            ('PASS_BY_REF', pass_by_ref),
            ('POINTER', pointer),
            ('CONDITIONAL', conditional),
            ('DOT', dot),
            ('ASSIGN', assign),                             # Other
            ('SEP', sep),
            ('END', e_n_d),
            ('AT_SYMBOL', at_symbol),
            ('SINGLE_COLON', single_colon),
            ('QUESTION_MARK', question_mark),
            ('DOLLAR_SIGN', dollar_sign),
            ('POUND', pound),
            ('QUOTE', quote),
            ('BACKSLASH', backslash),
            ('CP_RIGHT', cp_right),                         # Unicode
            ('EMPTY_SET', empty_set),
            ('EMPTY_SET_LC', empty_set_lc),
            ('B_SHARP', b_sharp),
            ('B_SHARP_LC', b_sharp_lc),
            ('NUMBER', number),                             # Regular
            ('ID', i_d),
            ('WHITESPACE', whitespace),
            ('ARITHMETIC_OP', arithmetic_op),
            ('MISMATCH', mismatch)                          # Trash
            ]
        t_string = '|'.join(('(?P<{}>{})'.format(pair[0], pair[1])
                             for pair in token_specification))
        self.tok_regex = re.compile(t_string, re.S | re.A)

    def tokenize(self, text):
        """Yield 3-tuples for every found match."""
        for token in self.tok_regex.finditer(text):
            yield Token(token.lastgroup, token.group(), token.span())

    def get_tokens(self, text):
        """Return a list of all tokens in the text."""
        return [token for token in self.tokenize(text)]

    def print_matches(self, code):
        """Test the tokenizer."""
        for token in self.tok_regex.finditer(code):
            print(token.lastgroup, end=' ')
            input(token.group())

    def match_lines(self, file):
        """Tracks what files have what lines.

        Take a set of lines from a file and the file's name,
        add the lines to line_matches.
        """
        for line in file.lineset.difference(self.total_lineset):
            self.line_matches[line] = [file.filename]
        for line in file.lineset.intersection(self.total_lineset):
            self.line_matches[line].append(file.filename)
        self.total_lineset = self.total_lineset.union(file.lineset)

    def print_output(self, outfile):
        """Print the line_matches dictionary to outfile."""
        print(outfile)
        with open(outfile, "w") as file:
            for k in self.line_matches:
                if len(self.line_matches[k]) > 1:
                    print(k, file=file)
                    print(self.line_matches[k], file=file)
                    # input(self.line_matches[k])
