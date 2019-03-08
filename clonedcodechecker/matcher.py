#!/usr/bin/env python3

import re


class matcher:

    def __init__(self):

        NUMBER = '[0-9]+[.]?[0-9]*'      # Integer or decimal number
        ASSIGN = '='                     # Assignment operator
        END = ';'                        # Statement terminator
        ID = '[A-Za-z_]+'                # Identifiers
        OP = '[+]|[-]|(?<!/)[*](?!/)|(?<!/)/(?!/)'  # Arithmetic operators
        WHITESPACE = '\s+'               # spaces, tabs, and newlines
        MISMATCH = '.'                   # Any other character

        token_specification = [
        ('NUMBER', NUMBER),
        ('ASSIGN', ASSIGN),
        ('END', END),
        ('ID', ID),
        ('OP', OP),
        ('WHITESPACE', WHITESPACE),
        ('MISMATCH', MISMATCH),
        ]
        te = '|'.join(('(?P<{}>{})'.format(pair[0], pair[1])
                       for pair in token_specification))
        self.tok_regex = re.compile(te)

    def printMatches(self, code):
        for token in self.tok_regex.finditer(code):
            print(token.lastgroup, end=' ')
            input(token.group())
